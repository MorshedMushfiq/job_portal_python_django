from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE= [
        ('recruiter',  'Recruiter'),
        ('seeker', 'Seeker'),
    ]

    user_type = models.CharField(choices=USER_TYPE, max_length=50, null=True)
    def __str__(self):
        return f"{self.username} - {self.user_type}"
    

class BasicInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    first_name =  models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email =  models.EmailField(max_length=100, null=True)
    designation = models.CharField(max_length=50, null=True)
    contact_no = models.CharField(max_length=50, null=True)
    career_summary = models.TextField(max_length=500, null=True)
    age = models.CharField(max_length=20, null=True)
    dob = models.DateField(max_length=40, null=True)
    picture = models.ImageField(max_length=100, null=True)
    GENDER_TYPE = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=100, choices=GENDER_TYPE, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.designation}"
    




