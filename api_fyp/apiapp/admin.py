from django.contrib import admin

# Register your models here.
from .models import Patient

@admin.register(Patient)
class GetPatientAdmin(admin.ModelAdmin):
    list_display = ['PTID', 'PTGENDER', 'PTRACCAT','FHQSIBAD','FHQSIBAD','DIAGNOSIS','DXDDUE','GENOTYPE','MMSCORE','AGE']