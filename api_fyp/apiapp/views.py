from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Patient
from .models import UserProfile
from django.contrib import messages 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import create_user



def home(request):
    return render(request, 'Home.html', {})

def patients(request):
    patients = Patient.objects.all()
    return render(request, 'patients.html', {"patients":patients})

def userprofile(request, pk):
    if request.user.is_authenticated:
        user_info = get_object_or_404(UserProfile, id=pk)
        return render(request, "dashboard.html", {"user_info" : user_info})
    else:
        return redirect('login')

# using django's inbuilt authenticate function to process the post form
def user_login(request):
    if request.method == "POST":
        username = request.POST['user_username']
        password = request.POST['user_password']
        user = authenticate(request,username= username, password = password)
        if user is not None:
            login(request, user)
            return redirect('userprofile', pk=user.pk)
    else: 
        return render(request, "login.html", {})
    return render(request, "login.html", {})
def user_logout(request):
    logout(request)
    return redirect('home')
def user_signup(request):
    form = create_user()
    if request.method =='GET':
        form = create_user()
    if request.method == 'POST':
        form = create_user(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            # user_form.username = user_form.username.lower()
            password_n = form.cleaned_data.get('password1')
            user_form.save()
            user = authenticate(username = user_form.username, password= password_n)
            login(request, user)
            return redirect('userprofile', pk=user.pk)
    return render(request, 'signup.html', {'form': form})

