from django.shortcuts import render

# Create your views here.

#write an api endpoint using drf that accepts all types of form bodies with any key values

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
import json
from .models import Form, FormFields, FormSubmissions
from .serializers import FormSerializer, FormFieldsSerializer, FormSubmissionsSerializer
from .utils import find_form_by_hash


class DynamicTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Delete existing token if it exists
        Token.objects.filter(user=user).delete()

        # Create a new token
        token = Token.objects.create(user=user)

        return Response({'token': token.key})


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Delete the user's token to logout
        Token.objects.filter(user=request.user).delete()
        return Response({
            "message": "Successfully logged out",
            "status": "success"
        }, status=status.HTTP_200_OK)


class FormViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Form instances.
    """
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Set the created_by and updated_by fields to the current user."""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """Set the updated_by field to the current user."""
        serializer.save(updated_by=self.request.user)


class FormFieldsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing FormFields instances.
    """
    queryset = FormFields.objects.all()
    serializer_class = FormFieldsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned fields to a given form,
        by filtering against a `form` query parameter in the URL.
        """
        queryset = FormFields.objects.all()
        form_id = self.request.query_params.get('form', None)
        if form_id is not None:
            queryset = queryset.filter(form__id=form_id)
        return queryset


class DynamicFormView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def send_form_submission_email(self, form, form_data):
        """
        Send an email notification about the form submission.

        Args:
            form: The Form instance that was submitted
            form_data: The submitted form data
        """
        # Format the form data for the email
        formatted_data = []
        for field_name, value in form_data.items():
            formatted_data.append(f"{field_name}: {value}")

        # Join the formatted data with line breaks
        data_text = "\n".join(formatted_data)

        # Prepare the email content
        subject = f"New Form Submission: {form.name}"
        message = f"""
A new submission has been received for the form: {form.name}

Form Details:
-------------
Form ID: {form.id}
Form Name: {form.name}
Form Description: {form.description or 'N/A'}

Submission Data:
---------------
{data_text}

This is an automated message.
"""

        # Send the email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['ammadhassanqureshi@gmail.com'],
            fail_silently=False
        )

    def get(self, request, *args, **kwargs):
        # Get the hashed form ID from the query parameters
        hashed_id = request.query_params.get('id')

        if not hashed_id:
            return Response({
                "message": "Form ID is required",
                "status": "error"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Look up the form by the hashed ID
        form = find_form_by_hash(hashed_id)
        if not form:
            return Response({
                "message": "Form not found",
                "status": "error"
            }, status=status.HTTP_404_NOT_FOUND)

        # Return the form details
        serializer = FormSerializer(form, context={'request': request})
        return Response({
            "message": "Form found",
            "form": serializer.data,
            "status": "success"
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Get the hashed form ID from the query parameters
        hashed_id = request.query_params.get('id')

        if not hashed_id:
            return Response({
                "message": "Form ID is required",
                "status": "error"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Look up the form by the hashed ID
        form = find_form_by_hash(hashed_id)
        if not form:
            return Response({
                "message": "Form not found",
                "status": "error"
            }, status=status.HTTP_404_NOT_FOUND)

        # Get the form fields
        form_fields = FormFields.objects.filter(form=form)

        # Validate the submitted data against the form fields
        data = request.data
        valid_fields = {field.field_mapping for field in form_fields}

        # Check if all required fields are present
        missing_fields = []
        for field in form_fields:
            if field.field_mapping not in data:
                missing_fields.append(field.field_mapping)

        if missing_fields:
            return Response({
                "message": "Missing required fields",
                "missing_fields": missing_fields,
                "status": "error"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Filter out any fields that are not in the form definition
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}

        # Create a new form submission
        submission_data = {
            'form': form.id,
            'data': filtered_data,
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT')
        }

        serializer = FormSubmissionsSerializer(data=submission_data)
        if serializer.is_valid():
            submission = serializer.save()

            # Send email notification about the form submission
            self.send_form_submission_email(form, filtered_data)

            return Response({
                "message": "Form submission successful",
                "submission": serializer.data,
                "status": "success"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "Invalid submission data",
                "errors": serializer.errors,
                "status": "error"
            }, status=status.HTTP_400_BAD_REQUEST)
