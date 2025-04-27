from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DynamicFormView, LogoutView, FormViewSet, FormFieldsViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'api/forms', FormViewSet)
router.register(r'api/form-fields', FormFieldsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/dynamic-form/', DynamicFormView.as_view(), name='dynamic-form'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
