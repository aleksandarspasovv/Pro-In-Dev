from django import forms
from ProInDev.content.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'media']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'body': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Write your post content here', 'maxlength': '2000'}
            ),
            'media': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body and len(body) > 2000:
            raise forms.ValidationError("Content cannot exceed 2000 characters.")
        return body


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here'}),
        }
