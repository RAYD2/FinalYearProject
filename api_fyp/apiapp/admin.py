from django.contrib import admin

# Register your models here.
from .models import Patient
from .models import Prediction

@admin.register(Patient)
class GetPatientAdmin(admin.ModelAdmin):
    list_display = ['SUBJECT_ID', 'MRI_ID', 'GENDER', 'HAND', 'GROUP', 'EDUCATION', 'SES', 'CDR', 'MMSCORE', 'AGE', 'ETIV', 'NWBV', 'ASF'
]

@admin.register(Prediction)
class GetPredictiontAdmin(admin.ModelAdmin):
    list_display = ['SUBJECT_ID','Prediction_Result']