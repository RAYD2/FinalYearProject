from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
#  model for the patient data

class Patient(models.Model):

    # Choices for Gender 
    GenderChoices = [
        (0,'Male'),
        (1, 'Female')
    ]
    
    # Choices for Dominant Hand 
    Dominant_H_Choices = [
        (0,'Right'),
        (1, 'Left')
    ]

    # Choices for Social Economic Status 
    CDR_Choices = [
        (0,'Non Demented'),
        (0.5, 'Very Mild AD'),
        (1, 'Mild AD'),
        (2, 'Moderate AD'),
    ]

    # Chices got Group
    Group_Choices = [
        (0,'Non Demented'),
        (1, 'Demented'),
        (2, 'Converted')
    ] 
  

    SUBJECT_ID = models.CharField(max_length=50, null=True, blank=False)
    MRI_ID = models.CharField(max_length=50, null=True, blank=False)
    GENDER = models.IntegerField(choices=GenderChoices, null=True, blank=False)
    HAND = models.IntegerField(choices=Dominant_H_Choices, null=True, blank=False)
    GROUP = models.IntegerField(choices=Group_Choices , null=True, blank=False)
    EDUCATION = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],null=True, blank=False)
    SES = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],null=True, blank=False)
    CDR = models.IntegerField(choices=CDR_Choices, null=True, blank=False)
    MMSCORE = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)],null=True, blank=False)
    AGE = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True, blank=False)
    ETIV = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)],null=True, blank=False)
    NWBV = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True, blank=False)
    ASF = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True, blank=False)
    
    def __str__(self):
        return self.SUBJECT_ID
    
class Prediction(models.Model):
    SUBJECT_ID = models.CharField(max_length=50, null=True, blank=False)
    Prediction_Result = models.CharField(max_length=50)

    def __str__(self):
        return self.SUBJECT_ID