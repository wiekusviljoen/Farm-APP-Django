from django import forms
from .models import Farm


class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        exclude = ('owner',)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }