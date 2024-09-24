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
    return render(req, 'common/profile.html')

@login_required
def logoutPage(req):
    logout(req)
    messages.success(req, 'Logout Successful!')
    return redirect('login')

@login_required
def home(req):
    return render(req,  'common/index.html')


@login_required
def logoutPage(req):
    logout(req)
    messages.success(req,  'Logged Out Successfully')
    return redirect('loginPage')


@login_required
def add_basic_info(req):
    
    if req.user.user_type == "seeker" or req.user.user_type == 'recruiter':
        if req.method == "POST":
            first_name = req.POST.get('fname')
            last_name = req.POST.get('lname')
            designation = req.POST.get('designation')
            
    
    
    
    return render(req, 'common/add_basic_info.html')









