from django import forms
from ProInDev.user_content.models import UserPost

class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ['title', 'body', 'media']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'media': forms.FileInput(attrs={'class': 'form-control'}),
        }
