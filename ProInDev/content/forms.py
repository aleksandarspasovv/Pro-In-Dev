from django import forms
from ProInDev.content.models import Post, Category, Comment


# Form for creating or editing a Post
class PostForm(forms.ModelForm):
    # Field for selecting multiple categories with checkboxes
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.none(),  # Placeholder queryset, updated in __init__
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',  # Adds Bootstrap styling
        }),
        required=True,
        label="Categories",  # Field label
    )

    class Meta:
        # Model associated with the form
        model = Post
        # Fields to include in the form
        fields = ['title', 'body', 'media', 'categories']
        # Custom widgets for styling and placeholders
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control rounded-pill shadow-sm',  # Adds Bootstrap styling
                'placeholder': 'Enter post title',  # Placeholder text
                'required': 'required',  # Mark field as required
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control rounded-3 shadow-sm',  # Adds Bootstrap styling
                'rows': 4,  # Number of rows in the textarea
                'maxlength': 2000,  # Maximum length for the body
                'placeholder': 'Write your post content here',  # Placeholder text
                'required': 'required',  # Mark field as required
            }),
            'media': forms.FileInput(attrs={
                'class': 'form-control rounded-3 shadow-sm',  # Adds Bootstrap styling
            }),
        }

    def __init__(self, *args, **kwargs):
        # Initialize the form and set the queryset for categories
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all()  # Populate with all categories
        self.fields['categories'].widget.attrs.update({
            'class': 'form-check-input',  # Update Bootstrap styling for checkboxes
        })

    def clean_categories(self):
        # Ensure at least one category is selected
        categories = self.cleaned_data.get('categories')
        if not categories:
            raise forms.ValidationError("Please select at least one category.")
        return categories

    def clean_body(self):
        # Validate the length of the body content
        body = self.cleaned_data.get('body')
        if body and len(body) > 2000:
            raise forms.ValidationError("Content cannot exceed 2000 characters.")
        return body

    def clean_media(self):
        # Validate the size of the uploaded media file
        media = self.cleaned_data.get('media')
        if media:
            max_size_kb = 330  # Maximum allowed size in KB
            if media.size > max_size_kb * 1024:
                raise forms.ValidationError(f"The uploaded image exceeds {max_size_kb} KB.")
        return media


# Form for creating a Comment
class CommentForm(forms.ModelForm):
    class Meta:
        # Model associated with the form
        model = Comment
        # Fields to include in the form
        fields = ['content']
        # Custom widget for styling and placeholder text
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',  # Adds Bootstrap styling
                'placeholder': 'Write your comment here',  # Placeholder text
            }),
        }
