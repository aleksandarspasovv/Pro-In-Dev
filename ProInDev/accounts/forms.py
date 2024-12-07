from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ProInDev.accounts.models import UserProfile


# User registration form class
class UserRegistrationForm(UserCreationForm):
    class Meta:
        # Model associated with the form
        model = User
        # Fields included in the form
        fields = ['username', 'email', 'password1', 'password2']

    # Save method for the form
    def save(self, commit=True):
        # Calls the original save method
        user = super().save(commit=commit)
        return user


# User profile form class
class UserProfileForm(forms.ModelForm):
    # First name field (optional)
    first_name = forms.CharField(
        max_length=30,
        required=False,
        label="First Name",
    )

    # Last name field (optional)
    last_name = forms.CharField(
        max_length=30,
        required=False,
        label="Last Name",
    )

    # Overview field (textarea, optional)
    overview = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Overview",
    )

    # GitHub link field (optional)
    github = forms.URLField(
        required=False,
        label="GitHub Link",
    )

    # Instagram link field (optional)
    instagram = forms.URLField(
        required=False,
        label="Instagram Link",
    )

    class Meta:
        # Model associated with the form
        model = UserProfile
        # Fields included in the form
        fields = [
            'bio',
            'profile_image',
            'github',
            'instagram',
        ]

    # Initialize the form
    def __init__(self, *args, **kwargs):
        # Extract the user object from the arguments (if provided)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Set initial values for first name and last name
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    # Validation method for the form data
    def clean(self):
        cleaned_data = super().clean()
        github = cleaned_data.get('github')
        instagram = cleaned_data.get('instagram')

        # Ensure at least one social media link is provided
        if not github and not instagram:
            raise forms.ValidationError("Please provide at least one social media link (GitHub or Instagram).")

        return cleaned_data

    # Save method for the form
    def save(self, commit=True):
        # Create a user profile instance without saving
        user_profile = super().save(commit=False)
        # Update the profile information
        user_profile.bio = self.cleaned_data.get('overview', user_profile.bio)
        user_profile.github = self.cleaned_data.get('github', user_profile.github)
        user_profile.instagram = self.cleaned_data.get('instagram', user_profile.instagram)

        # Save the profile if commit is True
        if commit:
            user_profile.save()

        return user_profile


# Custom authentication form class
class CustomAuthenticationForm(AuthenticationForm):
    # Method to confirm if the user is allowed to log in
    def confirm_login_allowed(self, user):
        if not user.is_active:
            # Raise a ValidationError if the account is inactive
            raise ValidationError(
                "This account is inactive.",
                code='inactive_account',
            )
