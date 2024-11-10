from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ProInDev.accounts.forms import UserRegistrationForm, UserProfileForm

class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'sign-up.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
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
    profile = request.user.userprofile
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
    profile = request.user.userprofile
    form = UserProfileForm(instance=profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    return render(request, 'settings.html', {'form': form})
