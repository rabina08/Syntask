# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from dashboard.forms import SignUpForm
from django.contrib.auth import logout

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html') 

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


# @login_required
# def dashboard_view(request):
#     return render(request, 'core/dashboard.html')

 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Replace 'dashboard' with your desired URL name
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})
   
def logout_view(request):
    logout(request)
    return redirect('login')  # redirect to login page after logging out