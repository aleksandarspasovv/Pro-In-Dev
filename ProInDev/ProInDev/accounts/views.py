from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
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
    profile, created = UserProfile.objects.get_or_create(user=request.user)
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
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(instance=profile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            profile.bio = form.cleaned_data['overview']
            form.save()

            messages.success(request, "Your profile was successfully updated.")
            return redirect('profile_edit')

        messages.error(request, "There was an error updating your profile.")

    return render(request, 'settings.html', {'form': form})


@login_required
def remove_account(request):
    if request.method == "POST":
        password = request.POST.get('password')
        user = request.user

        if authenticate(username=user.username, password=password):
            user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect('index')
        else:
            messages.error(request, "Password is incorrect. Account deletion failed.")
            return redirect('profile_edit')
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
