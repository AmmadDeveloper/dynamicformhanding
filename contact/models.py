from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.

class Form(models.Model):
    """
    Model to store form information including metadata about creation and updates.
    """
    name = models.CharField(max_length=255, help_text="Name of the form")
    description = models.TextField(blank=True, null=True, help_text="Description of the form")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the form was created")
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_forms',
        help_text="User who created the form"
    )
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the form was last updated")
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='updated_forms',
        help_text="User who last updated the form"
    )

    def __str__(self):
        return self.name


class FormFields(models.Model):
    """
    Model to store form fields with mapping to standard field types.
    Has a many-to-one relationship with the Form model.
    """
    FIELD_MAPPING_CHOICES = [
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('address_line_1', 'Address Line 1'),
        ('address_line_2', 'Address Line 2'),
        ('city', 'City'),
        ('country', 'Country'),
        ('zip', 'ZIP/Postal Code'),
        ('message', 'Message'),
    ]

    field_name = models.CharField(max_length=255, help_text="Name of the field")
    field_mapping = models.CharField(
        max_length=50, 
        choices=FIELD_MAPPING_CHOICES,
        help_text="Type of field (e.g., first_name, email, etc.)"
    )
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='fields',
        help_text="The form this field belongs to"
    )

    def __str__(self):
        return f"{self.form.name} - {self.field_name} ({self.get_field_mapping_display()})"


class FormSubmissions(models.Model):
    """
    Model to store form submissions.
    Has a many-to-one relationship with the Form model.
    """
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='submissions',
        help_text="The form this submission belongs to"
    )
    data = models.JSONField(help_text="The submitted form data")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the submission was created")
    ip_address = models.GenericIPAddressField(blank=True, null=True, help_text="IP address of the submitter")
    user_agent = models.TextField(blank=True, null=True, help_text="User agent of the submitter")

    def __str__(self):
        return f"Submission for {self.form.name} at {self.created_at}"
