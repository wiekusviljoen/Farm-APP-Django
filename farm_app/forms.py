from django import forms
from .models import Farm, ChatMessage


class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        exclude = ('owner',)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class ChatMessageForm(forms.Form):
    message = forms.CharField(
        label='Ask me anything about farming or animal feeds',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'e.g., What should I feed my pregnant cows? How do I prevent cattle diseases?',
            'class': 'form-control'
        })
    )