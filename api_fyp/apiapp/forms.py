from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from .models import Patient
from .models import Visit 

class create_user(UserCreationForm):
    email = forms.EmailField(label ="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Email Address"}))
    first_name = forms.CharField(label ="", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter First Name"}))
    last_name = forms.CharField(label ="", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter Last Name"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class create_new_patient(forms.ModelForm):
    PT_F_NAME = forms.CharField(label ="", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter First Name"}))
    PT_LAST_NAME = forms.CharField(label ="", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter Last Name"}))
    class Meta:
        model = Patient
        fields = ( 'PT_F_NAME', 'PT_LAST_NAME', 'SUBJECT_ID','GENDER', 'HAND')
        # 'GROUP', 'EDUCATION', 'SES', 'CDR', 'MMSCORE', 'AGE', 'ETIV', 'NWBV', 'ASF','MRI_ID',

class create_visit(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ('GROUP', 'EDUCATION', 'SES', 'CDR', 'MMSCORE', 'AGE', 'ETIV', 'NWBV', 'ASF')

