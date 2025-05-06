from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
# import that allows me to automatically create profile when user joins
from django.db.models.signals import post_save


# extending the django user profile
class User(AbstractUser):
    email = models.EmailField(unique = True)
    def __str__(self):
        return self.username
    
    def as_dict(self):
        return{
            'id': self.id,
            'password': self.password,
            'username': self.username,
            'email': self.email,
        }
# making a profile for each user 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    def __str__(self):
        return self.user.username
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

    PT_F_NAME = models.CharField(max_length=50, null=True, blank=False)
    PT_LAST_NAME = models.CharField(max_length=50, null=True, blank=False)
    SUBJECT_ID = models.CharField(max_length=50, null=True, blank=False, unique=True)
    GENDER = models.IntegerField(choices=GenderChoices, null=True, blank=False)
    HAND = models.IntegerField(choices=Dominant_H_Choices, null=True, blank=False)
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name= 'assigned_to',null=True, blank=True)
    flagged_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name= 'flagged_by',null=True, blank=True)
    def __str__(self):
        return self.SUBJECT_ID
# model for stored visits 
class Visit(models.Model):

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
    # maximum 6 visits for now 
    GROUP = models.IntegerField(choices=Group_Choices , null=True, blank=False)
    VISIT = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],null=True, blank=False)
    EDUCATION = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],null=True, blank=False)
    SES = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],null=True, blank=False)
    CDR = models.FloatField(choices=CDR_Choices, null=True, blank=False)
    MMSCORE = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)],null=True, blank=False)
    AGE = models.IntegerField(validators=[MinValueValidator(0)],null=True, blank=False)
    ETIV = models.FloatField(validators=[MinValueValidator(0)],null=True, blank=False)
    NWBV = models.FloatField(validators=[MinValueValidator(0)],null=True, blank=False)
    ASF = models.FloatField(validators=[MinValueValidator(0)],null=True, blank=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name= 'visits',null=False, blank=True)

    def __str__(self):
        return str(self.id)
# predictions are stored within this model once made, keeping a log of previous predictions
class Prediction(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name= 'prediction',null=True, blank=True)
    Prediction_Result = models.JSONField(null=True, blank=True)
    Risk_prediction = models.CharField(max_length =100,null=True, blank =True)
    # Prediction_Result = models.CharField(max_length =100,null=True, blank=False)
    DATE_PREDICTED = models.DateTimeField(null=True, blank=False)

    def __str__(self):
        return str(self.id)
# mri images are saved in this model  
class MRI_IMG(models.Model):
    patient_img = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name= 'MRI_image',null=True, blank=True)
    # on image upload media dir and imgs sub dir created
    MRI_ID = models.CharField(max_length=50, null=True, blank=False, unique=True)
    img = models.ImageField(null=True, blank=True,upload_to='imgs/')
    def __str__(self):
        return str(self.id)
# function creates a new user using the instance passed into it 
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()
post_save.connect(create_user_profile, sender = User)
