"""
Module for handling form-related functionality in Django.

This module provides classes and utilities for working with forms in Django applications.
"""
from django import forms


class CategoryForm(forms.Form):
    """
    A form for handling category data.

    This form allows users to submit category URLs.

    Attributes:
        url (URLField): A URL field representing the category URL.
            This field is rendered as a hidden input in the form.
    """
    url = forms.URLField(widget=forms.HiddenInput())
