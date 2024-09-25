from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from  django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from App.models import *


def register(req):
    if req.method=='POST':
        uname = req.POST.get('uname')
        email = req.POST.get('email')
        password = req.POST.get('pass')
        user_type =  req.POST.get('user_type')
        confirm_password = req.POST.get('con_pass')
        if not all([uname, email, user_type, password, confirm_password]):
            messages.error(req, 'Please fill all the fields')
            return render(req, 'common/register.html')
        try: 
            validate_email(email)
        except ValidationError:
            messages.error(req, 'Invalid email')
            return render(req, 'common/register.html')

        if password != confirm_password:
            messages.error(req,  "Password & Confirm Password Not Matched!")
            return render(req, 'common/register.html')
        if len(password)<8:
            messages.error(req,  "Password should be at least 8 characters!")
            return render(req, 'common/register.html')
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            messages.warning(req, 'Password must contain at least one letter and one number')
            return render(req, 'common/register.html')
        try:
            user = CustomUser.objects.create_user(username=uname, email=email, user_type=user_type, password=confirm_password)
            messages.success(req,  'User Created Successfully')
            return redirect('loginPage')
        except IntegrityError:
            messages.error(req, 'Username already exists')
            return render(req, 'common/register.html')


    return render(req, 'common/register.html')     



def loginPage(req):
    if req.method == 'POST':
        username = req.POST.get('uname')
        password = req.POST.get('pass')
        if not all([username, password]):
            messages.error(req, 'Please fill all the fields')
            return render(req, 'common/login.html')
        else: 
            user = authenticate(username=username, password=password)
            user =  authenticate(username=username, password=password)
            if user is not None:
                login(req, user)
                messages.success(req, 'Login Success!')
                return redirect('home')
            else: 
                messages.warning(req,  'Invalid Credentials')
                return render(req, 'common/login.html')

    return render(req, 'common/login.html')


@login_required
def home(req):
    return render(req, 'common/index.html')

@login_required
def contact(req):
    return render(req, 'common/contact.html')


@login_required
def browse_jobs(req):
    return render(req, 'common/browse_jobs.html')

@login_required
def add_skills(req):
    return render(req, 'common/add_skill.html')



@login_required
def profile(req):
    data = CustomUser.objects.get(id=req.user.id)
    
    
    try:
        basic_info = get_object_or_404(BasicInfo, user=req.user)
        
    except Http404:
        messages.warning(req, "you don't have any basic information, please add information")
        return render(req, 'common/profile.html')

    context = {
        'data':data,
        'basic_info':basic_info
    }

    return render(req, 'common/profile.html', context)

@login_required
def logoutPage(req):
    logout(req)
    messages.success(req, 'Logout Successful!')
    return redirect('login')

@login_required
def home(req):
    return render(req, 'common/index.html')
    return render(req,  'common/index.html')


@login_required
def logoutPage(req):
    logout(req)
    messages.success(req,  'Logged Out Successfully')
    return redirect('loginPage')


@login_required
def add_basic_info(req):
    
    if req.user.user_type == "seeker" or req.user.user_type == 'recruiter':
        current_user = req.user
        if req.method == "POST":
            first_name = req.POST.get('first_name')
            last_name = req.POST.get('last_name')
            designation = req.POST.get('designation')
            contact_no = req.POST.get('contact_no')
            career_summary = req.POST.get('career_summary')
            age = req.POST.get('age')
            dob = req.POST.get('dob')
            picture = req.FILES.get('picture')
            gender = req.POST.get('gender')
            
            add_basic_info = BasicInfo(
                user=current_user,
                designation = designation,
                contact_no = contact_no,
                email = current_user.email,
                career_summary = career_summary,
                age = age,
                dob = dob,
                picture = picture,
                gender = gender,
            )
            
            current_user.first_name=first_name
            current_user.last_name=last_name

            current_user.save()
            
            add_basic_info.save()
            messages.success(req, "Basic Info Added Successfully")
            return redirect('profile')
            
    
    return render(req, 'common/add_basic_info.html',{'data':current_user})

def edit_basic_info(req, id):
    current_user = req.user
    try: 
        data = get_object_or_404(BasicInfo, id=id)
    except Http404:
        messages.warning(req, "You have some problem to go to the edit option page.")
        return redirect('profile')    
    
    if req.user.user_type == "seeker" or req.user.user_type == 'recruiter':
        current_user = req.user
        if req.method == "POST":
            id = req.POST.get('basic_info_id')
            first_name = req.POST.get('first_name')
            last_name = req.POST.get('last_name')
            designation = req.POST.get('designation')
            contact_no = req.POST.get('contact_no')
            career_summary = req.POST.get('career_summary')
            age = req.POST.get('age')
            dob = req.POST.get('dob')
            picture_new = req.FILES.get('picture_new')
            picture_old = req.POST.get('picture_old')
            gender = req.POST.get('gender')
            
            basic_info_update = BasicInfo(
                id = id,
                user=current_user,
                designation = designation,
                contact_no = contact_no,
                email = current_user.email,
                career_summary = career_summary,
                age = age,
                dob = dob,
                gender = gender,
            )
            if  picture_new:
                basic_info_update.picture = picture_new
            else:
                basic_info_update.picture = picture_old
            current_user.first_name=first_name
            current_user.last_name=last_name

            current_user.save()
            
            basic_info_update.save()
            messages.success(req, "Basic Info Updated Successfully")
            return redirect('profile')
                    
        

    
    context = {
        'data':data
    }
    
    return render(req, 'common/edit_basic_info.html', context)

def my_settings(req):
    current_user = req.user
    return render(req, 'common/settings.html')









