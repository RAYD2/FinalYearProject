from django.contrib import admin

# Register your models here.
from .models import Patient
from .models import Prediction
from .models import User
from .models import UserProfile
from .models import Visit
from .models import MRI_IMG

@admin.register(Patient)
class GetPatientAdmin(admin.ModelAdmin):
    list_display = ['SUBJECT_ID', 'GENDER', 'HAND']


@admin.register(Prediction)
class GetPredictiontAdmin(admin.ModelAdmin):
    list_display = ['patient','Prediction_Result', 'DATE_PREDICTED']

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
    list_display = ['VISIT','GROUP', 'EDUCATION', 'SES', 'CDR', 'MMSCORE', 'AGE', 'ETIV', 'NWBV', 'ASF']
   
@admin.register(MRI_IMG)
class GetUserProfile(admin.ModelAdmin):
    list_display = ['MRI_ID']
    pass