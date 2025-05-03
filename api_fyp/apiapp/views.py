from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
from .models import UserProfile
from django.contrib import messages 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import create_user
from .forms import create_new_patient
from .models import Visit
from .forms import create_visit
from django.http import JsonResponse
import pandas as pd
from google.oauth2 import service_account
import google.auth.transport.requests
from sklearn.preprocessing import MinMaxScaler
import json
import requests
import re
import json
import numpy as np
import requests
from django.utils import timezone
from google.auth import load_credentials_from_file
from google.auth.transport.requests import Request
from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import Prediction
import datetime
from django.core.serializers import serialize
from django.template.loader import render_to_string
from django.db.models import Q
from .forms import create_MRI

# rendering the home page 
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'Home.html', {})
# rendering the profile page with the user information
def profile(request: HttpRequest, pk) -> HttpResponse:
    user_info = get_object_or_404(UserProfile, id=pk)
    return render(request, 'Profile.html', {"user_info": user_info})

def userprofile(request: HttpRequest, pk) -> HttpResponse:
    if request.user.is_authenticated:
        user_info = get_object_or_404(UserProfile, id=pk)
        return JsonResponse({"user_info" : user_info})
    else:
        return redirect('login')

# using django's inbuilt authenticate function to process the post form
def user_login(request: HttpRequest) -> HttpResponse:
    # getting the login page 
    if request.method == "GET":
        return render(request, 'login.html')
    # andling submission
    elif request.method == "POST":
        username = request.POST['user_username']
        password = request.POST['user_password']
        user = authenticate(request,username= username, password = password)
        if user is not None:
            login(request, user)
            return redirect('dash_view', pk=user.pk)
    else: 
        return JsonResponse({'error': "login not successful"})

def user_logout(request):
    logout(request)
    return redirect('home')

def user_signup(request):
    if request.method =='GET':
        form = create_user()
        return render(request, 'signup.html', {'form': form})
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
    return JsonResponse({'error': "signup not successful"})

def patients(request, pk):
    # form to add patients 
    user_info = get_object_or_404(UserProfile, id=pk)
    query = request.GET.get('query_value')
    if query:
        query = query.split()
        fields = Q()
        for i in query:
            fields |= Q(PT_F_NAME__icontains= i)
            fields |= Q(PT_LAST_NAME__icontains= i)
            fields |= Q(SUBJECT_ID__icontains= i)
        patients = Patient.objects.filter(fields)
        patients_list = list(patients.values())
    else:
        patients = Patient.objects.filter(assigned_to__isnull = True)
        patients_list = list(patients.values())
    if request.method == 'GET':
        form = create_new_patient()
        if request.headers.get('X-Requested-With')== 'XMLHttpRequest' and request.GET.get('action') == 'get_form':
            form_b = render_to_string('patient.html', {'form':form}, request)
            return JsonResponse({'form': form_b})
        return render(request,'patients.html', {
            'patients': patients_list,
            'user_info': user_info , 
            'form': form
        })
    elif request.method == 'POST'and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = create_new_patient(request.POST)
        if form.is_valid():
            patient = form.save()
            form = create_new_patient()
            # return redirect('patients', pk = patient.pk)
        # patients = Patient.objects.filter(assigned_to__isnull = True)
        # patients_list = list(patients.values())
        return JsonResponse({
            "patients": patients_list,
            'id': patient.id,
            'SUBJECT_ID': patient.SUBJECT_ID,
            'MRI_ID': patient.MRI_ID, 
            'GENDER': patient.GENDER, 
            'HAND':patient.HAND
        })
    else:
       form = create_new_patient( request.POST)
       if form.is_valid():
            patient = form.save()
            return redirect('patients', pk=pk )

    # only patients that are not already assigned show up
    return render(request, 'patients.html', {'user_info': user_info, 'form':create_new_patient(), "patients": patients_list})

def dash_view(request, pk):
    if request.user.is_authenticated:
        try:
            user_info = get_object_or_404(UserProfile, id=pk)
            profile = UserProfile.objects.get(user=request.user)
            current_patients = Patient.objects.filter(assigned_to = profile)
            flagged_patients = Patient.objects.filter(flagged_by=profile)
            print(flagged_patients, profile)
            return render(request, "dashboard.html", {"current_patients" : current_patients, "user_info" : user_info, "flagged_patients" : flagged_patients})
        except:
                current_patients = Patient.objects.none()
                flagged_patients = Patient.objects.none()
    else:
       current_patients= Patient.objects.none()
       flagged_patients = Patient.objects.none()
    
    return render(request, "dashboard.html", {"current_patients" : current_patients, "user_info" : user_info , "flagged_patients" : flagged_patients})

def patient_add_list(request, pk):
    add_patient = Patient.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=request.user)
    add_patient.assigned_to = profile
    add_patient.save()
    return redirect('patients', pk=profile.pk)

def patient_dashboard(request, pk , p_pk):
    patient_info = get_object_or_404(Patient, id=p_pk)
    user_info = get_object_or_404(UserProfile, id=pk)
    patient_visits = Visit.objects.filter(patient = patient_info).order_by('VISIT')
    prediction_patient = Prediction.objects.filter(patient = patient_info).order_by('DATE_PREDICTED').last()
    current_diagnosis = Visit.objects.filter(patient = patient_info).order_by('VISIT').last()
    if request.method == 'GET':
        form = create_visit()
        form_mri = create_MRI()
        if request.headers.get('X-Requested-With')== 'XMLHttpRequest' and request.GET.get('action') == 'get_form':
            form_b = render_to_string('patient_dashboard.html', {'form':form}, request)
            return JsonResponse({'form': form_b})
        return render(request, 'patient_dashboard.html', {'form': form, 'form_mri': form_mri, 'patient_info': patient_info,'user_info': user_info,'patient_visits': patient_visits ,"predictions": prediction_patient,"current_diagnosis":current_diagnosis})
    elif request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = create_visit(request.POST)
        if form.is_valid():
            visit_form = form.save(commit=False)
            visit_form.patient = patient_info
            form.save()
            form = create_visit() 
            # prediction = None
        else:
            print("no valid ")
        patient_visits_list = list(patient_visits.values())
        return JsonResponse({
            "patient_visits": patient_visits_list
        })
    else:
       form = create_visit(request.POST)
       if form.is_valid():
            visit_form = form.save(commit=False)
            visit_form.patient = patient_info
            form.save()
            return redirect('patient_dashboard', pk=pk, p_pk =p_pk )
       else:
            return render(request, 'patient_dashboard.html', {'form': form,'form_mri' :form_mri,  'patient_info': patient_info,'user_info': user_info,'patient_visits': patient_visits ,"predictions": prediction_patient,"current_diagnosis":current_diagnosis})
    
def add_img(request, pk , p_pk):
    patient_info = get_object_or_404(Patient, id=p_pk)
    user_info = get_object_or_404(UserProfile, id=pk)
    patient_visits = Visit.objects.filter(patient = patient_info).order_by('VISIT')
    prediction_patient = Prediction.objects.filter(patient = patient_info).order_by('DATE_PREDICTED').last()
    current_diagnosis = Visit.objects.filter(patient = patient_info).order_by('VISIT').last()
    if request.method == 'GET':
        form = create_MRI()
        form_visit = create_visit()
        if request.headers.get('X-Requested-With')== 'XMLHttpRequest' and request.GET.get('action') == 'get_form':
            form_m = render_to_string('patient_dashboard.html', {'form_mri': form}, request)
            return JsonResponse({'form': form_m})
        return render(request, 'patient_dashboard.html', {'form_mri': form, 'form':form_visit,'patient_info': patient_info,'user_info': user_info,'patient_visits': patient_visits ,"predictions": prediction_patient,"current_diagnosis":current_diagnosis})
    elif request.method == "POST":
        form = create_MRI(request.POST, request.FILES)
        if form.is_valid():
                mri_form = form.save(commit=False)
                mri_form.patient_img = patient_info
                mri_form.save()
                return redirect('patient_dashboard', pk=pk, p_pk =p_pk )
        else:
            form = create_MRI() 
            return render(request, 'patient_dashboard.html', {'form_mri': form, 'patient_info': patient_info,'user_info': user_info,'patient_visits': patient_visits ,"predictions": prediction_patient,"current_diagnosis":current_diagnosis})

    return redirect('patient_dashboard', pk=pk, p_pk =p_pk )


def patient_remove_list(request, pk):
    patient = Patient.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=request.user)
    patient.assigned_to = None
    patient.save()
    if  patient.flagged_by == profile:
        patient.flagged_by = None
        patient.save()
    
    return redirect('dash_view',  pk=profile.pk)


def patient_flag(request, pk):
    flag_patient = Patient.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=request.user)
    if flag_patient.flagged_by == None:
            flag_patient.flagged_by = profile
            flag_patient.save()
    else:
            flag_patient.flagged_by = None
            flag_patient.save()
    return redirect('patient_dashboard', pk=profile.id, p_pk =pk )

def prediction_view(request, pk, p_pk):
    patient_info = get_object_or_404(Patient, id=p_pk)
    user_info = get_object_or_404(UserProfile, id=pk)
    patient_visits = Visit.objects.filter(patient = patient_info).order_by('VISIT')
    try:
        prediction = prediction_LSTM(request, pk , p_pk)
        predictions = risk_filter(prediction)
        final_risk = predictions[-1]
        print("made it")
        add_prediction = Prediction.objects.create(patient = patient_info, Prediction_Result = prediction, DATE_PREDICTED = timezone.now(), Risk_prediction = final_risk )
        add_prediction.save()
    except Exception as e:
        print("CANT GET PREDICTION: ERROR")
        messages.error(request, "Prediction not avaliable")
    return redirect('patient_dashboard', pk=pk, p_pk =p_pk )

def risk_filter(p):
    predictions_risk = []
    values = p['predictions']
    print(values)
    for i in values:
        for j in i:
            if j <= 0.3:
                predictions_risk.append('low')
            elif 0.3 < j <= 0.8:
                predictions_risk.append('medium')
            elif 0.8 < j:
                predictions_risk.append('high')
    print("risks", predictions_risk)
    return predictions_risk


# LSTM

#  sending data 

    # getting the data from the database

def get_encoded_LSTM(request, pk, p_pk):
    patient_info = get_object_or_404(Patient, id=p_pk)
    user_info = get_object_or_404(UserProfile, id=pk)
    patient_visits = Visit.objects.filter(patient = patient_info).order_by('VISIT')
    data = list(patient_visits.values())
    # list of db values are turned into a dataframe
    # adding a column for their gender
    df = pd.DataFrame(data)
    # patient_info = patient_info.reset_index(drop= True)
    df['Gender'] = patient_info.GENDER
    df = df.drop('patient_id', axis=1 )
    print(df)
    # this data frame is passes through a fucntion which normalises it and turns them into timesteps (same script used in training)
    # df = supervised(df, input_TS=1,output_TS=1,dropnan=True)
    df = normalise(df)

    return df
def normalise(df):

# normalisation of the df features
    new_scale = MinMaxScaler(feature_range = (0,1))
    scaled_df = new_scale.fit_transform(df)
    # using the supervised method to frame the df as supervised learning
    supervised_df = supervised(scaled_df, 1, 1)
    # isolating the feature we want to predict, resulting in 8 input variables/ 1 target (output variable aka group)
    supervised_df = supervised_df.drop(['var2(t)','var3(t)', 'var4(t)', 'var5(t)', 'var6(t)', 'var7(t)', 'var8(t)', 'var9(t)', 'var10(t)', 'var11(t)', 'var12(t)'],axis = 1)
    # print(supervised_df)
    return supervised_df
# framing the supervised learning problem as prediciting the likleyhood of developing AD
def supervised(data, input_TS = 1, output_TS = 1, dropnan = True):
  # getting the number of features within the dataset
  num_features = 1 if type(data) is list else data.shape[1]
  # assigning them to a dataframe and making two empty lists for data/feature names
  df = pd.DataFrame(data)
  col_data, col_names = list(), list()
  # past time steps
  for i in range(input_TS, 0, -1):
    col_data.append(df.shift(i))
    col_names += [('var%d(t-%d)'% (j + 1, i )) for j in range(num_features)]

  # future time steps

  for i in range(0, output_TS):
    col_data.append(df.shift(-i))
    if i == 0:
      col_names += [('var%d(t)'% (j + 1 )) for j in range(num_features)]
    else:
      col_names += [('var%d(t-%d)'% (j + 1, i )) for j in range(num_features)]
#  concatenating the past and future time steps into one df

  result_df = pd.concat(col_data, axis = 1)
  result_df.columns = col_names

  # dropping entries with missing values

  if dropnan:
    result_df.dropna(inplace = True)
  print("result",result_df)
  return result_df

# getting prediction from LSTM
def prediction_LSTM(request, pk , p_pk):
    # print("WEVE MADE CONTACT")
    input_ds = get_encoded_LSTM(request, pk, p_pk)
    # reshaping and turning results into a list (MUST fit format of model input)
    input_values = input_ds.values
    input_np = input_values.reshape((input_values.shape[0], 1, input_values.shape[1])) 
    input_new = input_np.tolist()
    input_ds = {
            "instances": input_new
    }
    # print(input_ds)
    print("GOT THE DATA")
    cred_path = 'api_fyp/arctic-compass-457720-e8-fdadfe37776f.json'
    print("heloo")
    # credentials, _ =  load_credentials_from_file('api_fyp/arctic-compass-457720-e8-fdadfe37776f.json') 
    credentials = service_account.Credentials.from_service_account_file(cred_path, scopes =['https://www.googleapis.com/auth/cloud-platform'])
    print("HERRE")
    credentials.refresh(google.auth.transport.requests.Request())
    cred_token = credentials.token
    if not cred_token:
        print("no token :()")
    print("HER")
    endpoint_link =f"https://us-central1-aiplatform.googleapis.com/v1/projects/{948712763405}/locations/us-central1/endpoints/{1073779757151158272}:predict"
    # defining the headers request
    headers = {
        "Authorization":  f"Bearer {cred_token}",
        "Content-Type": "application/json"
    }
        # sending the data to the models cloud endpoint from IOT application
    response = requests.post(endpoint_link, headers=headers, json=input_ds)

    # getting the response, handling errors

    if response.status_code == 200:
        predicted = response.json()
        
        print(predicted)
        return predicted

    else:
        print("ERROR: COULDN'T GET PREDICTION", response.text)
        return None


