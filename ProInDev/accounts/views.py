from datetime import date
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ProInDev.accounts.forms import UserRegistrationForm, UserProfileForm
from ProInDev.accounts.models import UserProfile


# Handles user registration with GET and POST methods
class RegisterView(View):
    def get(self, request):
        # Display the registration form
        form = UserRegistrationForm()
        return render(request, 'sign-up.html', {'form': form})

    def post(self, request):
        # Process the registration form
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user and redirect to login
            user = form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        # Show error messages if registration fails
        messages.error(request, "Registration failed. Please correct the errors below.")
        return render(request, 'sign-up.html', {'form': form})


# Handles user login with GET and POST methods
class LoginView(View):
    def get(self, request):
        # Display the login form
        form = AuthenticationForm()
        return render(request, 'sign-in.html', {'form': form})

    def post(self, request):
        # Process the login form
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Log the user in and redirect to the index page
            user = form.get_user()
            login(request, user)
            return redirect('index')
        # Show error messages if login fails
        messages.error(request, "Invalid username or password.")
        return render(request, 'sign-in.html', {'form': form})


# Displays and updates the logged-in user's profile
@login_required
def profile_view(request):
    # Get or create the user's profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(instance=profile)
    if request.method == 'POST':
        # Handle profile update
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save the updated profile
            form.save()
            messages.success(request, "Your profile was successfully updated.")
            return redirect('profile')
        # Show error messages if update fails
        messages.error(request, "There was an error updating your profile.")
    return render(request, 'my-profile.html', {'form': form})


# Allows users to edit their profile information
@login_required
def profile_edit(request):
    # Get or create the user's profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(instance=profile, user=request.user)

    if request.method == 'POST':
        # Handle profile edit submission
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            # Update the user model with first and last names
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', user.first_name)
            user.last_name = form.cleaned_data.get('last_name', user.last_name)
            user.save()

            # Update the profile model with other details
            profile.bio = form.cleaned_data.get('overview', profile.bio)
            profile.github = form.cleaned_data.get('github', profile.github)
            profile.instagram = form.cleaned_data.get('instagram', profile.instagram)
            profile.save()

            messages.success(request, "Your profile was successfully updated.")
            return redirect('profile_edit')

        # Show error messages if update fails
        messages.error(request, "There was an error updating your profile.")

    return render(request, 'settings.html', {'form': form})


# Allows users to deactivate their account
@login_required
def remove_account(request):
    if request.method == "POST":
        # Authenticate the user's password before deactivation
        password = request.POST.get('password')
        user = request.user

        if authenticate(username=user.username, password=password):
            # Deactivate the user account
            user.is_active = False
            user.save()
            messages.success(request, "Your account has been deactivated.")
            logout(request)
            return redirect('index')
        else:
            # Show error if password is incorrect
            messages.error(request, "Password is incorrect. Account deactivation failed.")
            return redirect('profile_edit')


# Allows users to change their password
@login_required
def change_password(request):
    if request.method == 'POST':
        # Process the password change form
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Save the new password and update session
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been successfully updated.")
            return redirect('profile_edit')
        else:
            # Show error messages if password change fails
            messages.error(request, "There was an error changing your password. Please check the form and try again.")
    else:
        # Display the password change form
        form = PasswordChangeForm(request.user)
    return render(request, 'settings.html', {'form': form})


# Displays another user's public profile
def profile_view_user(request, user_id):
    # Get the user object by ID
    user = get_object_or_404(User, id=user_id)
    return render(request, 'profile.html', {'user': user})


# Handles profile image uploads with restrictions
@login_required
def profile_image_upload(request):
    user_profile = request.user.userprofile

    if request.method == "POST" and request.FILES.get("profile_image"):
        # Check if the user can change the profile image
        if not user_profile.can_change_profile_image():
            messages.error(request, "You can only change your profile picture up to 3 times per week.")
            return redirect("profile")

        profile_image = request.FILES["profile_image"]

        # Ensure the profile image size does not exceed 330 KB
        if profile_image.size > 330 * 1024:
            messages.error(request, "Profile picture size must not exceed 330 KB.")
            return redirect("profile")

        # Save the new profile image
        user_profile.profile_image = profile_image
        user_profile.change_count += 1
        user_profile.last_change_date = date.today()
        user_profile.save()
        messages.success(request, "Profile image updated successfully!")
    else:
        # Show error if upload fails
        messages.error(request, "Failed to upload profile image.")

    return redirect("profile")
