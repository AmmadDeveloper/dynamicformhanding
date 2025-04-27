from django.contrib import admin
from .models import Form, FormFields, FormSubmissions

# Register your models here.
@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'created_by', 'updated_at', 'updated_by')
    list_filter = ('created_at', 'updated_at', 'created_by', 'updated_by')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at', 'created_by', 'updated_at', 'updated_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FormFields)
class FormFieldsAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'field_mapping', 'form')
    list_filter = ('field_mapping', 'form')
    search_fields = ('field_name', 'form__name')
    fieldsets = (
        (None, {
            'fields': ('form', 'field_name', 'field_mapping')
        }),
    )


@admin.register(FormSubmissions)
class FormSubmissionsAdmin(admin.ModelAdmin):
    list_display = ('form', 'created_at', 'ip_address')
    list_filter = ('form', 'created_at')
    search_fields = ('form__name', 'ip_address')
    readonly_fields = ('created_at', 'data_display')

    def data_display(self, obj):
        """Display the JSON data in a more readable format."""
        import json
        from django.utils.safestring import mark_safe
        if obj.data:
            # Pretty print the JSON data
            formatted_data = json.dumps(obj.data, indent=2)
            # Convert to HTML with <pre> tags for formatting
            return mark_safe(f'<pre>{formatted_data}</pre>')
        return '-'

    data_display.short_description = 'Form Data'

    fieldsets = (
        (None, {
            'fields': ('form', 'data_display', 'created_at')
        }),
        ('Submission Metadata', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
