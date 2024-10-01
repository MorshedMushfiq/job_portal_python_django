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
    picture = models.ImageField(upload_to="media/user_profile", null=True)
    GENDER_TYPE = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=100, choices=GENDER_TYPE, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.designation}"
class FieldOfStudyModel(models.Model):
    name =  models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

class DegreeModel(models.Model):
    Degree=[
        ('bachelors', 'Bachelors'),
        ('masters', 'Masters'),
        ('phd', 'Phd'),
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma')
    ]

    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    level  = models.CharField(max_length=100, choices=Degree, null=True)

    def __str__(self):
        return f"{self.name} - {self.level}"


class InstituteNameModel(models.Model):
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    postal_code = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    website = models.URLField(null=True)
    established_year = models.PositiveIntegerField(null=True)
    contact_number = models.CharField(max_length=50, null=True)

    class Meta:
        unique_together = ['name', 'established_year']

    def __str__(self):
        return f"{self.name} - {self.contact_number}"


    
class EducationModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    institution_name = models.CharField(max_length=50, null=True)
    degree = models.CharField(max_length=50, null=True)
    field_of_study = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    class meta: 
        unique_together = ['user', 'institution_name', 'degree']


    

class SkillModel(models.Model):
    skill_proficiency = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert')
    ]

    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE, null=True)
    skill_name = models.CharField(max_length=100, null=True)
    skill_level = models.CharField(max_length=50, choices=skill_proficiency, null=True)

    class Meta: 
        unique_together = ['user', 'skill_name']


    def __str__(self):
        return f"{self.user.username} - {self.skill_name}"
    
class IntermediateSkillModel(models.Model):
    skill_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.skill_name}"    

class ExperienceModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    job_title = models.CharField(max_length=50, null=True)
    company_name = models.CharField(max_length=50, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    description = models.TextField(null=True)
    def __str__(self):
        return f"{self.user.username} - {self.job_title} - {self.end_date}"


class InterestModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    interest_name = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=5000, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.interest_name}"
    

class LanguageModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    language_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.language_name}"


class JobModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    job_title = models.CharField(max_length=50, null=True)
    job_description = models.TextField(null=True)
    job_location = models.CharField(max_length=100, null=True)
    company_name = models.CharField(max_length=50, null=True)
    company_logo = models.ImageField(upload_to="media/job/company_logo", null=True)
    JOB_TYPE = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),

    ]

    job_type = models.CharField(max_length=100, choices=JOB_TYPE, null=True)
    salary = models.PositiveBigIntegerField(null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True)
    application_deadline = models.DateField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.job_title}"


class ApplyNow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE, null=True)
    applicant_name = models.CharField(max_length=80, null=True)
    applicant_email = models.EmailField(max_length=80, null=True)
    applicant_resume = models.FileField(upload_to="media/files/resumes", null=True)
    applicant_cover_letter = models.TextField(null=True)

    class Meta:
        unique_together = ['user', 'job']

    def __str__(self):
        return f"{self.user.username} - {self.job.job_title} - {self.applicant_email}"
        




