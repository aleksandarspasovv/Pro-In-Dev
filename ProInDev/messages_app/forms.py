from django import forms
from .models import Message


class MessageForm(forms.ModelForm):  # Form for creating or editing a message
    class Meta:
        model = Message  # Associates the form with the Message model
        fields = ['receiver', 'content']  # Fields to include in the form
