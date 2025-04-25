from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Patient
from .models import UserProfile
from django.contrib import messages 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import create_user
from .forms import create_new_patient



def home(request):
    return render(request, 'Home.html', {})

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
            return redirect('dash_view', pk=user.pk)
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
            return redirect('dash_view', pk=user.pk)
    return render(request, 'signup.html', {'form': form})

# functions to get patient details/ add patients/edit their information


def patients(request, pk):
    # form to add patients 
    user_info = get_object_or_404(UserProfile, id=pk)
    patients = Patient.objects.filter(assigned_to__isnull = True)
    form = create_new_patient()
    if request.method == 'POST':
        form = create_new_patient(request.POST)
        if form.is_valid():
            patient =  form.save()
            # return redirect('patients', pk = patient.pk)
        patients = Patient.objects.filter(assigned_to__isnull = True)
    # only patients that are not already assigned show up
    return render(request, 'patients.html', {'form': form,'patients': patients, 'user_info': user_info})

def patient_information(request, pk):
    patient_info = get_object_or_404(Patient, id=pk)
    return render(request, "patient_dashboard.html", {"patient_info" : patient_info})

def dash_view(request, pk):
    if request.user.is_authenticated:
        try:
            user_info = get_object_or_404(UserProfile, id=pk)
            profile = UserProfile.objects.get(user=request.user)
            current_patients = Patient.objects.filter(assigned_to = profile)
            return render(request, "dashboard.html", {"current_patients" : current_patients, "user_info" : user_info})
        except:
                current_patients = Patient.objects.none()
    else:
       current_patients= Patient.objects.none()
    
    return render(request, "dashboard.html", {"current_patients" : current_patients, "user_info" : user_info})

def patient_add_list(request, pk):
    add_patient = Patient.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=request.user)
    add_patient.assigned_to = profile
    add_patient.save()
    return redirect('patients', pk=profile.pk)

def patient_dashboard(request):
    return render(request, 'patient_dashboard.html', {})