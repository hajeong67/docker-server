from django import forms
from .models import Wheel

class WheelUploadForm(forms.ModelForm):
    class Meta:
        model = Wheel
        fields = ['whl_file']
        widgets = {
            'whl_file': forms.ClearableFileInput(attrs={'accept': '.whl'}),
        }