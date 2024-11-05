from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views import View
from ProInDev.accounts.forms import UserRegistrationForm, UserProfileForm
from ProInDev.accounts.models import UserProfile
from django.contrib.auth.decorators import login_required

class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'sign-up.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('index')
        return render(request, 'sign-up.html', {'form': form})

class LoginView(View):
    def get(self, request):
        return render(request, 'sign-in.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'sign-in.html', {'error': 'Invalid credentials'})

@login_required
def profile_view(request):
    profile = request.user.userprofile
    form = UserProfileForm(instance=profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'my-profile.html', {'form': form})
