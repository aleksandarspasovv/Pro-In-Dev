import os
from datetime import date
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from ProInDev.accounts.forms import UserRegistrationForm, UserProfileForm
from ProInDev.accounts.models import UserProfile


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'sign-up.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        messages.error(request, "Registration failed. Please correct the errors below.")
        return render(request, 'sign-up.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'sign-in.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        messages.error(request, "Invalid username or password.")
        return render(request, 'sign-in.html', {'form': form})


@login_required
def profile_view(request):
    User = get_user_model()
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    form = UserProfileForm(instance=profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was successfully updated.")
            return redirect('profile')
        messages.error(request, "There was an error updating your profile.")
    return render(request, 'my-profile.html', {'form': form})


@login_required
def profile_edit(request):
    User = get_user_model()
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        github = request.POST.get('github', '').strip()
        instagram = request.POST.get('instagram', '').strip()
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        if github:
            profile.github = github
        if instagram:
            profile.instagram = instagram
        profile.save()
        messages.success(request, "Your profile was successfully updated.")
        return redirect('profile_edit')
    return render(request, 'settings.html', {'user': user})


@login_required
def remove_account(request):
    if request.method == "POST":
        password = request.POST.get('password')
        user = request.user
        if authenticate(request=request, username=user.username, password=password):
            user.is_active = False
            user.save()
            messages.success(request, "Your account has been deactivated.")
            logout(request)
            return redirect('index')
        else:
            messages.error(request, "Password is incorrect. Account deactivation failed.")
            return redirect('profile_edit')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been successfully updated.")
            return redirect('profile_edit')
        else:
            messages.error(request, "There was an error changing your password. Please check the form and try again.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'settings.html', {'form': form})


def profile_view_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    return render(request, 'profile.html', {'user': user})


class CloudinaryError:
    pass


@login_required
def profile_image_upload(request):
    user_profile = request.user.userprofile

    if request.method == "POST" and request.FILES.get("profile_image"):
        if not user_profile.can_change_profile_image():
            messages.error(request, "You can only change your profile picture up to 3 times per week.")
            return redirect("profile")

        profile_image = request.FILES["profile_image"]

        if profile_image.size > 330 * 1024:
            messages.error(request, "Profile picture size must not exceed 330 KB.")
            return redirect("profile")

        try:
            user_profile.profile_image = profile_image
            user_profile.change_count += 1
            user_profile.last_change_date = date.today()
            user_profile.save()
            messages.success(request, "Profile image updated successfully!")
        except CloudinaryError as e:
            messages.error(request, f"Failed to upload profile image: {e}")
            return redirect("profile")
        except Exception as e:
            messages.error(request, "An unexpected error occurred while updating your profile image. Please try again.")
            return redirect("profile")
    else:
        messages.error(request, "No image selected for upload.")

    return redirect("profile")

