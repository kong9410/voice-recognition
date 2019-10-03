from django import forms
from django.forms import ClearableFileInput
from .models import UploadFileModel

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFileModel
        fields = ['files']
        widgets = {
            'files':ClearableFileInput(attrs={'multiple': True}),
        }