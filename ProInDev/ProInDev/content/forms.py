from django import forms
from ProInDev.content.models import Content, Comment

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'body']

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if len(body) > 2000:
            raise forms.ValidationError("Content cannot exceed 2000 characters.")
        return body


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
