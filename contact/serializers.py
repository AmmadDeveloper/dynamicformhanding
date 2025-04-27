from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Form, FormFields, FormSubmissions
from .utils import hash_id

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model, used in nested representations."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class FormFieldsSerializer(serializers.ModelSerializer):
    """Serializer for the FormFields model."""
    field_mapping_display = serializers.CharField(source='get_field_mapping_display', read_only=True)

    class Meta:
        model = FormFields
        fields = ['id', 'field_name', 'field_mapping', 'field_mapping_display', 'form']
        read_only_fields = ['id']
        extra_kwargs = {'form': {'required': False}}  # Make form field optional for nested serializer


class FormSerializer(serializers.ModelSerializer):
    """Serializer for the Form model."""
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    fields = FormFieldsSerializer(many=True, read_only=True)
    form_fields = FormFieldsSerializer(many=True, write_only=True, required=False)  # New field for input
    submission_url = serializers.SerializerMethodField(read_only=True)  # URL for form submission

    class Meta:
        model = Form
        fields = ['id', 'name', 'description', 'created_at', 'created_by', 
                 'updated_at', 'updated_by', 'fields', 'form_fields', 'submission_url']
        read_only_fields = ['created_at', 'updated_at', 'fields', 'submission_url']

    def get_submission_url(self, obj):
        """
        Generate a URL for form submission with a hashed form ID.
        """
        request = self.context.get('request')
        if request is None:
            return None

        # Get the base URL (scheme + host)
        base_url = request.build_absolute_uri('/').rstrip('/')

        # Generate a hashed ID
        hashed_id = hash_id(obj.id)

        # Return the full URL
        return f"{base_url}/api/dynamic-form/?id={hashed_id}"

    def create(self, validated_data):
        """
        Create a new Form instance with nested form fields.
        Sets the created_by and updated_by fields to the current user.
        """
        form_fields_data = validated_data.pop('form_fields', [])
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['updated_by'] = user

        # Create the form instance
        form = Form.objects.create(**validated_data)

        # Create form fields
        for field_data in form_fields_data:
            FormFields.objects.create(form=form, **field_data)

        return form

    def update(self, instance, validated_data):
        """
        Update a Form instance with nested form fields.
        Sets the updated_by field to the current user.
        """
        form_fields_data = validated_data.pop('form_fields', [])
        user = self.context['request'].user
        validated_data['updated_by'] = user

        # Update the form instance
        instance = super().update(instance, validated_data)

        # Create new form fields
        for field_data in form_fields_data:
            FormFields.objects.create(form=instance, **field_data)

        return instance


class FormSubmissionsSerializer(serializers.ModelSerializer):
    """Serializer for the FormSubmissions model."""
    form_name = serializers.CharField(source='form.name', read_only=True)

    class Meta:
        model = FormSubmissions
        fields = ['id', 'form', 'form_name', 'data', 'created_at', 'ip_address', 'user_agent']
        read_only_fields = ['id', 'created_at']
