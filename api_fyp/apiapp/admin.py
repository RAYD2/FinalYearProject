from django.contrib import admin

# Models are registered on this page
# imported models
from .models import Patient
from .models import Prediction
from .models import User
from .models import UserProfile
from .models import Visit
from .models import MRI_IMG

# patient and relative fields is registered to admin to view and edit
@admin.register(Patient)
class GetPatientAdmin(admin.ModelAdmin):
    list_display = ['SUBJECT_ID', 'GENDER', 'HAND']

# prediction and relative fields is registered to admin to view and edit
@admin.register(Prediction)
class GetPredictiontAdmin(admin.ModelAdmin):
    list_display = ['patient','Prediction_Result', 'DATE_PREDICTED']

# combining the user and their userprofile 
class UserProfileInline(admin.StackedInline):
    model = UserProfile
# User and relative fields is registered to admin to view and edit
@admin.register(User)
class GetUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    search_field = ['username']
    inlines = [UserProfileInline]
# User profile and the relevant fields
@admin.register(UserProfile)
class GetUserProfile(admin.ModelAdmin):
    list_display = ['user']
# visit and relative fields is registered to admin to view and edit
@admin.register(Visit)
class GetUserProfile(admin.ModelAdmin):
    list_display = ['GROUP','VISIT', 'EDUCATION', 'SES', 'CDR', 'MMSCORE', 'AGE', 'ETIV', 'NWBV', 'ASF']
# mri model and relative fields is registered to admin to view and edit
@admin.register(MRI_IMG)
class GetUserProfile(admin.ModelAdmin):
    list_display = ['MRI_ID']
    pass