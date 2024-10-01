"""
URL configuration for myProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginPage, name='loginPage'),
    path('logout/', logoutPage, name='logoutPage'),
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('contact/', contact, name='contact'),
    path('browse_jobs/', browse_jobs, name='browse_jobs'),
    path('profile/', profile, name='profile'),
    path('my_settings/', my_settings, name='my_settings'),
    path('add_skills/', add_skills, name='add_skills'),
    path('delete_skill/<int:id>', deleteSkill, name='delete_skill'),
    path('edit_skill/<int:id>', edit_skills, name='edit_skill'),
    path('add_admin_skills/', admin_add_skill, name='admin_add_skill'),
    path('field_of_study/', field_of_study, name='field_of_study'),
    path('degree/', degree, name='degree'),
    path('institute_add/', institute_add, name='institute_add'),
    path('add_education/', add_education, name='add_education'),
    path('delete_education/<int:id>', deleteEducation, name='delete_education'),
    path('edit_education/<int:id>', editEducation, name='edit_education'),
    path('add_experience/', addExperience, name='add_experience'),
    path('delete_experience/<int:id>', deleteExperience, name='delete_experience'),
    path('edit_experience/<int:id>', editExperience, name='edit_experience'),
    path('add_language/', addLanguage, name='add_language'),
    path('delete_language/<int:id>', deleteLanguage, name='delete_language'),
    path('edit_language/<int:id>', editLanguage, name='edit_language'),
    path('add_interest/', addInterest, name='add_interest'),
    path('delete_interest/<int:id>', deleteInterest, name='delete_interest'),
    path('edit_interest/<int:id>', editInterest, name='edit_interest'),
    path('add_basic_info/', add_basic_info, name='add_basic_info'),
    path('edit_basic_info/<int:id>', edit_basic_info, name='edit_basic_info'),

    path('add_skills/', add_skills, name='add_skills'),
    path('change_password/', changePassword, name='change_password'),
    path('add_job/', add_job, name='add_job'),
    path('created_jobs_by_recruiter',  recruiter_jobs_view, name='created_jobs_by_recruiter'),
    path('delete_job/<int:id>',  delete_job, name='delete_job'),
    path('edit_job/<int:id>',  edit_job, name='edit_job'),
    path('single_view_job/<int:id>',  single_view_job, name='single_view_job'),
    path('search_job/', search_job, name='search_job'),
    path('add_basic_info/', add_basic_info, name='add_basic_info'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


