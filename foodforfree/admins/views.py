from django.shortcuts import render, redirect


# Create your views here.
def homepage(request):
    return render(request, 'accounts/homepage.html')


def dashboard(request):
    return render(request, 'admins/dashboard.html')
