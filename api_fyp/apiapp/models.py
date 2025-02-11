from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
#  model for the patient data

class Patient(models.Model):

    # Choices for Gender 
    GenderChoices = [
        (1,'Male'),
        (2, 'Female')
    ]
    # Choices for racial categories 
    RacialCat= [
        (1,'American Indian or Alaskan Native'),
        (2, 'Asian'),
        (3, 'Native Haiwaian or other Pacific Islander'),
        (4,'Black or African American'),
        (5,'White'),
        (6, 'More than once race'),
        (7, 'Uknown'),
        (8, 'Native American'),
        (9, 'Other Pacific Islander')
    ]
    # Choices for Family History
    FHChoices = [
        (0, 'No'),
        (1, 'Yes'),
        (2, 'Unknown')
    ]
    DS_Choices = [
        (1,'CN'),
        (2,'MCI'),
        (3,'DEMENTIA')
    ]
    DXD_Choices = [
        (0,'Unknown'),
        (1, 'AD'),
        (2, 'NOT AD')
    ]
    GENO_Choices = [
        (0, '2/2'),
        (1, '2/3'),
        (2, '2/4'),
        (3, '3/3'),
        (4, '3/4'),
        (5, '4/4')
    ]


    PTID = models.CharField(max_length=50, null=True, blank=False)
    PTGENDER = models.IntegerField(choices=GenderChoices, null=True, blank=False)
    PTRACCAT = models.IntegerField(choices=RacialCat,null=True, blank=False)
    FHQSIBAD = models.IntegerField(choices=FHChoices,null=True, blank=False)
    DIAGNOSIS = models.IntegerField(choices=DS_Choices,null=True, blank=False)
    DXDDUE = models.IntegerField(choices= DXD_Choices,null=True, blank=False)
    GENOTYPE = models.IntegerField(choices=GENO_Choices,null=True, blank=False)
    MMSCORE = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)],null=True, blank=False)
    AGE = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True, blank=False)

    def __str__(self):
        return self.PTID