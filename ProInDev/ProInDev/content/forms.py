from django import forms
from ProInDev.content.models import Post, Category, Comment


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        }),
        required=True,
        label="Categories",
    )

    class Meta:
        model = Post
        fields = ['title', 'body', 'media', 'categories']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all()

    def clean_categories(self):
        categories = self.cleaned_data.get('categories')
        if not categories:
            raise forms.ValidationError("Please select at least one category.")
        return categories

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body and len(body) > 2000:
            raise forms.ValidationError("Content cannot exceed 2000 characters.")
        return body

    def clean_media(self):
        media = self.cleaned_data.get('media')
        if media:
            max_size_kb = 330
            if media.size > max_size_kb * 1024:
                raise forms.ValidationError(f"The uploaded image exceeds {max_size_kb} KB.")

        return media


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here'}),
        }
