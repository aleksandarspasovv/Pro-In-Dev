from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ProInDev.accounts.models import UserProfile


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        return user


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        label="First Name",
    )

    last_name = forms.CharField(
        max_length=30,
        required=False,
        label="Last Name",
    )

    overview = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Overview",
    )

    github = forms.URLField(
        required=False,
        label="GitHub Link",
    )

    instagram = forms.URLField(
        required=False,
        label="Instagram Link",
    )

    class Meta:
        model = UserProfile
        fields = [
            'bio',
            'profile_image',
            'github',
            'instagram',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def clean(self):
        cleaned_data = super().clean()
        github = cleaned_data.get('github')
        instagram = cleaned_data.get('instagram')

        if not github and not instagram:
            raise forms.ValidationError("Please provide at least one social media link (GitHub or Instagram).")

        return cleaned_data

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user_profile.bio = self.cleaned_data.get('overview', user_profile.bio)
        user_profile.github = self.cleaned_data.get('github', user_profile.github)
        user_profile.instagram = self.cleaned_data.get('instagram', user_profile.instagram)

        if commit:
            user_profile.save()

        return user_profile


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                "This account is inactive.",
                code='inactive_account',
            )
