from django import forms
from ProInDev.content.models import Content

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'body', 'visibility']
