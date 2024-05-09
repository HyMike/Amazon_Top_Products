from django import forms


class CategoryForm(forms.Form):
    url = forms.URLField(widget=forms.HiddenInput())
