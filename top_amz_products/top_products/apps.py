"""
django import from appconfig 
"""
from django.apps import AppConfig


class TopProductsConfig(AppConfig):
    """
    Django application configuration for the 'top_products' app.

    This AppConfig class defines configuration options for the 'top_products' app,
    including the default auto-generated primary key field and the app name.

    Attributes:
        default_auto_field (str): The name of the default auto-generated primary key field.
            This field is set to 'django.db.models.BigAutoField' to use a big integer field
            as the primary key for models in the 'top_products' app.
        name (str): The name of the Django app, which is set to 'top_products'.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "top_products"
