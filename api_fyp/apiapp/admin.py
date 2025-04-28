from django.contrib import admin

# Register your models here.
from .models import Patient
from .models import Prediction
from .models import User
from .models import UserProfile
from .models import Visit

@admin.register(Patient)
class GetPatientAdmin(admin.ModelAdmin):
    list_display = ['SUBJECT_ID', 'MRI_ID', 'GENDER', 'HAND']


@admin.register(Prediction)
class GetPredictiontAdmin(admin.ModelAdmin):
    list_display = ['SUBJECT_ID','Prediction_Result']

# combining the user and their userprofile 
class UserProfileInline(admin.StackedInline):
    model = UserProfile

@admin.register(User)
class GetUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    search_field = ['username']
    inlines = [UserProfileInline]

@admin.register(UserProfile)
class GetUserProfile(admin.ModelAdmin):
    list_display = ['user']
   
@admin.register(Visit)
class GetUserProfile(admin.ModelAdmin):
    list_display = ['GROUP', 'EDUCATION', 'SES', 'CDR', 'MMSCORE', 'AGE', 'ETIV', 'NWBV', 'ASF']
   
