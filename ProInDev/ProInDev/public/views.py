from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def privacy_and_terms(request):
    return render(request, 'privacy-and-terms.html')


def help_view(request):
    return render(request, 'help.html')
