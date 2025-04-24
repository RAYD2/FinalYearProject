from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class create_user(UserCreationForm):
    email = forms.EmailField(label ="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Email Address"}))
    first_name = forms.CharField(label ="", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter First Name"}))
    last_name = forms.CharField(label ="", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter Last Name"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
