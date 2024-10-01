from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from  django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import check_password
from django.db.models import Q

from App.models import *

# for register page with validation
def register(req):
    if req.user:
        return redirect('home')
    else:
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


# for login page with validation
def loginPage(req):
    if req.user:
        return redirect('home')
    else:
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

# for home page
@login_required
def home(req):
    jobs = JobModel.objects.all()
    context = {
        'data':jobs
    }
    return render(req, 'common/index.html', context)
# for contact page
@login_required
def contact(req):
    return render(req, 'common/contact.html')

# for jon feed
@login_required
def browse_jobs(req):
    jobs = JobModel.objects.all()
    context = {
        'data':jobs
    }
    return render(req, 'common/browse_jobs.html', context)


# add skill functionality
@login_required
def add_skills(req):
    current_user = req.user
    if req.user.user_type == "recruiter" or req.user.user_type == "seeker":
        all_skills = IntermediateSkillModel.objects.all()
        
        context = {
            'all_skills': all_skills
        }
        if req.method == 'POST':
            skill_id = req.POST.get('skill_id')
            skill_level = req.POST.get('skill_level')
            skill_obj = get_object_or_404(IntermediateSkillModel, id=skill_id)
            if SkillModel.objects.filter(user=current_user, skill_name=skill_obj).exists():
                messages.warning(req, 'This skill is already added.')
                return render(req, 'common/add_skill.html')
            else: 
                skill_add = SkillModel(
                    user = current_user,
                    skill_name = skill_obj.skill_name,
                    skill_level = skill_level
                )

                skill_add.save()
                return redirect('my_settings')
    return render(req, 'common/add_skill.html', context)

def deleteSkill(req, id):
    data = SkillModel.objects.get(id=id)
    data.delete()
    messages.success(req, "Skill Deleted Success")
    return redirect('my_settings')


def edit_skills(req, id):
    current_user = req.user
    if req.user.user_type == "recruiter" or req.user.user_type == "seeker":
        all_skills = IntermediateSkillModel.objects.all()
        skills = get_object_or_404(SkillModel, id=id)
        skill_id = skills.id
        print(skill_id)
        
        context = {
            'all_skills': all_skills,
            'skill':skills,
        }
        if req.method == 'POST':
            skill_id = req.POST.get('skill_id')
            id = req.POST.get('id')
            skill_level = req.POST.get('skill_level')
            skill_obj = get_object_or_404(IntermediateSkillModel, id=skill_id)
            if SkillModel.objects.filter(user=current_user, skill_name=skill_obj).exists():
                messages.warning(req, 'This skill is already added.')
                return render(req, 'common/edit_skill.html')
            else: 
                skill_update = SkillModel(
                    user = current_user,
                    id = id,
                    skill_name = skill_obj.skill_name,
                    skill_level = skill_level
                )

                skill_update.save()
                messages.success(req, 'Skill updated.')
                return redirect('my_settings')
    return render(req, 'common/edit_skill.html', context)





# admin add skill  functionality


def admin_add_skill(req):
    if req.method == 'POST':
        skill_name = req.POST.get('skill_name')
        admin_skill = IntermediateSkillModel(
            skill_name = skill_name
        )
        admin_skill.save()
        return redirect("my_settings")
    
    return render(req, "common/admin_add_skill.html")

 


# user profile functionality
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

# logout  functionality

@login_required
def logoutPage(req):
    logout(req)
    messages.success(req, 'Logout Successful!')
    return redirect('loginPage')

# add basic information  functionality
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



# edit and update basic info functionality
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

# my settings functionality
def my_settings(req):
    current_user = req.user
    skills = SkillModel.objects.all()
    education = EducationModel.objects.all()
    experience = ExperienceModel.objects.all()
    language = LanguageModel.objects.all()
    interest = InterestModel.objects.all()

    context = {
        'skills':skills,
        'education':education,
        'experience':experience,
        'language':language,
        'interest':interest

    }
    return render(req, 'common/settings.html', context)

# field of study  functionality
def  field_of_study(req):
    current_user = req.user
    if current_user.user_type == 'recruiter':

        if req.method == "POST":
            field_of_study = req.POST.get('field_of_study')
            field_desc = req.POST.get('decsription')
            field_study_create = FieldOfStudyModel(
                name = field_of_study,
                description = field_desc

            )
            field_study_create.save()
            messages.success(req, "Field of Study Added Successfully")
            return redirect('my_settings')
    else: 
        messages.error(req, "you are not authorized user")  
        return redirect('my_settings')
    return render(req,  'common/field_of_study.html')


# degree functionlity
def degree(req):
    current_user = req.user
    if current_user.user_type == 'recruiter':
        if req.method == "POST":
            degree_name = req.POST.get('degree_name')
            degree_desc = req.POST.get('desc')
            degree_level = req.POST.get('degree_level')
            degree_create = DegreeModel(
                name =  degree_name,
                description = degree_desc,
                level = degree_level,            
            )

            degree_create.save()
            messages.success(req, 'Degree Added Successful!')
            return redirect('my_settings')
    return render(req, 'common/add_degree.html')


# institute functionailty
def institute_add(req):
    if req.user.user_type == "recruiter":
        current_user = req.user
    try: 
        if req.method == "POST":
            name = req.POST.get('institute_name')
            address = req.POST.get('address')
            city = req.POST.get('city')
            state = req.POST.get('state')
            postal_code = req.POST.get('postal_code')
            country = req.POST.get('country')
            website = req.POST.get('website')
            established_year = req.POST.get('established_year')
            contact_number = req.POST.get('contact_number')

            institute_create = InstituteNameModel(
                name = name,
                address = address,
                city = city,
                state = state,
                postal_code = postal_code,
                country = country,
                website = website,
                established_year = established_year,
                contact_number = contact_number
            ) 

            institute_create.save()
            messages.success(req, "Institute Added Success")
            return redirect('my_settings')
    except IntegrityError:
        messages.error(req, "This data is already added.")
        return render(req, "common/add_institute.html")

    return render(req, "common/add_institute.html")

# add education functionality

def add_education(req):
    if req.user.user_type == "recruiter":
        degree = DegreeModel.objects.all()
        
        current_user = req.user
        try: 
            if req.method == "POST":
                institution_name = req.POST.get('institute_name')
                degree = req.POST.get('degree')
                field_of_study = req.POST.get('field_of_study')
                start_date = req.POST.get('start_date')
                end_date = req.POST.get('end_date')

                education_add = EducationModel(
                    user = current_user,
                    institution_name = institution_name,
                    degree = degree,
                    field_of_study = field_of_study,
                    start_date = start_date,
                    end_date = end_date

                )

                education_add.save()
                messages.success(req, "Education Added Success")
                return redirect('my_settings')
        except IntegrityError:
            messages.error(req, "Education is already exists")
            return render(req, "common/add_education.html")            

    context = {
        "degree":degree,

    }

    return render(req, "common/add_education.html", context)

def deleteEducation(req, id):
    data = EducationModel.objects.get(id=id)
    data.delete()
    messages.success(req, "Education Deleted Success")
    return redirect('my_settings')

def editEducation(req, id):
    if req.user.user_type == "recruiter":
        degree = DegreeModel.objects.all()
        current_user = req.user
        try: 
            data = get_object_or_404(EducationModel, id=id)
            if req.method == "POST":
                institution_name = req.POST.get('institute_name')
                id = req.POST.get('education_id')
                degree = req.POST.get('degree')
                field_of_study = req.POST.get('field_of_study')
                start_date = req.POST.get('start_date')
                end_date = req.POST.get('end_date')

                education_add = EducationModel(
                    user = current_user,
                    id = id,
                    institution_name = institution_name,
                    degree = degree,
                    field_of_study = field_of_study,
                    start_date = start_date,
                    end_date = end_date

                )

                education_add.save()
                messages.success(req, "Education Updated Success")
                return redirect('my_settings')
        except IntegrityError:
            messages.error(req, "Education is already exists")
            return render(req, "common/add_education.html")            

    context = {
        "degree":degree,
        'education':data,


    }

    return render(req, "common/edit_education.html", context)



def addExperience(request):
    if request.user.user_type == "recruiter":
        current_user = request.user
        try: 
            if request.method == "POST":
                job_title = request.POST.get('job_title')
                company_name = request.POST.get('company_name')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                description = request.POST.get('description')

                experience_add = ExperienceModel(
                    user = current_user,
                    job_title = job_title,
                    company_name = company_name,
                    start_date = start_date,
                    end_date = end_date,
                    description = description

                )

                experience_add.save()
                messages.success(request, "Experience Added Success")
                return redirect('my_settings')
        except IntegrityError:
            messages.error(request, "Experience is already exists")
            return render(request, "common/add_experience.html") 

    return render(request, "common/add_experience.html")

def deleteExperience(req, id):
    data = ExperienceModel.objects.get(id=id)
    data.delete()
    messages.success(req, "Experience Deleted Success")
    return redirect('my_settings')



def editExperience(request, id):
    if request.user.user_type == "recruiter":
        current_user = request.user
        try: 
            data = get_object_or_404(ExperienceModel, id=id)
            if request.method == "POST":
                job_title = request.POST.get('job_title')
                id = request.POST.get('experience_id')
                company_name = request.POST.get('company_name')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                description = request.POST.get('description')

                experience_add = ExperienceModel(
                    user = current_user,
                    id = id,
                    job_title = job_title,
                    company_name = company_name,
                    start_date = start_date,
                    end_date = end_date,
                    description = description

                )

                experience_add.save()
                messages.success(request, "Experience Updated Success")
                return redirect('my_settings')
        except IntegrityError:
            messages.error(request, "Experience is already exists")
            return render(request, "common/edit_experience.html")

    context = {
        'experience':data
    }     

    return render(request, "common/edit_experience.html", context)










def addLanguage(request):

    if request.user.user_type == "recruiter":
        current_user = request.user
    try: 
        data = get_object_or_404(LanguageModel, id=id)
        if request.method == "POST":
            language_name = request.POST.get('language_name')

            language_add = LanguageModel(
                user = current_user,
                language_name = language_name,
            )

            language_add.save()
            messages.success(request, "Language Added Success")
            return redirect('my_settings')
    except IntegrityError:
        messages.error(request, "Language is already exists")
        return render(request, "common/add_experience.html") 

    context = {
        'language':data
    }

    return render(request, "common/add_language.html", context)

def deleteLanguage(req, id):
    data = LanguageModel.objects.get(id=id)
    data.delete()
    messages.success(req, "Language Deleted Success")
    return redirect('my_settings')


def editLanguage(req, id):
    current_user = req.user
    try: 
        data = get_object_or_404(LanguageModel, id=id)
    except Http404:
        messages.warning(req, "You have some problem to go to the edit option page.")
        return redirect('my_settings')   
    if req.method == "POST":
        language_name = req.POST.get('language_name')
        id = req.POST.get('language_id')

        update_language = LanguageModel(
            user = current_user,
            id = id,
            language_name = language_name,

        )
        update_language.save()
        messages.success(req, "Language Updated Success")
        return redirect('my_settings')
    
    context = {
        'language':data
    }
    return render(req, "common/edit_language.html", context)











def addInterest(request):
    if request.user.user_type == "recruiter":
        current_user = request.user
    try: 
        if request.method == "POST":
            interest_name = request.POST.get('interest_name')
            description = request.POST.get('description')

            interest_add = InterestModel(
                user = current_user,
                interest_name = interest_name,
                description = description,
            )

            interest_add.save()
            messages.success(request, "Interest Added Success")
            return redirect('my_settings')
    except IntegrityError:
        messages.error(request, "Interest is already exists")
        return render(request, "common/add_interest.html") 



    return render(request, "common/add_interest.html")



def deleteInterest(req, id):
    data =  InterestModel.objects.get(id=id)
    data.delete()
    messages.success(req, "Interest Deleted Success")
    return redirect('my_settings')

def editInterest(req, id):
    current_user = req.user
    try: 
        data = get_object_or_404(InterestModel, id=id)
    except Http404:
        messages.warning(req, "You have some problem to go to the edit option page.")
        return redirect('my_settings')   
    if req.method == "POST":
        interest_name = req.POST.get('interest_name')
        description = req.POST.get('description')
        id = req.POST.get('interest_id')

        update_interest = InterestModel(
            user = current_user,
            id = id,
            interest_name = interest_name,
            description = description,

        )

        update_interest.save()
        messages.success(req, "Interest Updated Success")
        return redirect('my_settings')
    
    context = {
        'interest':data
    }

    return render(req, "common/edit_interest.html", context)


def changePassword(req):
    current_user = req.user
    if req.method == "POST":
        old_password = req.POST.get('old_password')
        new_password = req.POST.get('new_password')
        confirm_password = req.POST.get('confirm_password')

        if check_password(old_password, current_user.password):
            if new_password != confirm_password:
                messages.error(req, "New Password And Confirm Password Doesn't Match.")
                return render(req,  "common/change_password.html")
            elif old_password == new_password or old_password == confirm_password:
                messages.error(req, "Old Password And New Password Can't Be Same.")
                return render(req,  "common/change_password.html")
            else:
                current_user.set_password(confirm_password)
                current_user.save()
                messages.success(req, "Password Reset Success")
                return render(req,  "common/change_password.html")

    return render(req,  "common/change_password.html")


def add_job(req):
    if req.user.user_type == "recruiter":
        current_user = req.user
        if req.method == "POST":
            job_title = req.POST.get('job_title')
            job_description = req.POST.get('job_description')
            job_location = req.POST.get('job_location')
            job_type = req.POST.get('job_type')
            salary = req.POST.get('salary')
            company_name = req.POST.get('company_name')
            company_logo = req.FILES.get('company_logo')
            application_deadline = req.POST.get('application_deadline')
            
            job_add = JobModel(
                user = current_user,
                job_title=job_title,
                job_description=job_description,
                job_location=job_location,
                job_type=job_type,
                salary=salary,
                company_name=company_name,
                company_logo=company_logo,
                application_deadline=application_deadline,
            )

            job_add.save()
            messages.success(req, "Job Added Successfully")
            return redirect("created_jobs_by_recruiter")
        
    return render(req, "common/add_job.html")


def recruiter_jobs_view(req):
    if req.user.user_type == "recruiter":
        current_user = req.user
        jobs = JobModel.objects.filter(user=current_user)
        
    return render(req, "common/createdJobsByRecruiter.html", {"jobs": jobs})


def delete_job(req, id):
    if req.user.user_type == "recruiter":
        current_user = req.user
        job = get_object_or_404(JobModel, user=current_user, id=id)
        job.delete()
        messages.success(req, "Job Deleted Successfully")
        return redirect('created_jobs_by_recruiter')
    
def edit_job(req, id):
    if req.user.user_type == "recruiter":
        current_user = req.user
        job = get_object_or_404(JobModel, user=current_user, id=id)
        if req.method == "POST":
            job_title = req.POST.get('job_title')
            id = req.POST.get('job_id')
            job_description = req.POST.get('job_description')
            job_location = req.POST.get('job_location')
            job_type = req.POST.get('job_type')
            salary = req.POST.get('salary')
            company_name = req.POST.get('company_name')
            company_logo_new = req.FILES.get('company_logo_new')
            company_logo_old = req.POST.get('company_logo_old')
            application_deadline = req.POST.get('application_deadline')
            
            job_update = JobModel(
                user = current_user,
                id = id,
                job_title=job_title,
                job_description=job_description,
                job_location=job_location,
                job_type=job_type,
                salary=salary,
                company_name=company_name,
                application_deadline=application_deadline,
            )

            if company_logo_new:
                job_update.company_logo = company_logo_new
            else:
                job_update.company_logo = company_logo_old    

            job_update.save()
            messages.success(req, "Job Updated Successfully")
            return redirect("created_jobs_by_recruiter")
    



    context = {
            "job":job
    }
    return render(req, "common/edit_job.html", context)

def single_view_job(req, id):
    single_job = JobModel.objects.get(id=id)
    current_user = req.user
    current_job = JobModel.objects.get(id=id)
    already_applied = ApplyNow.objects.filter(user=current_user, job=id)
    if req.method == "POST":
        if already_applied.exists():
            messages.error(req, "You have Already Applied This Job")
            return render(req, "common/single_view_job.html", context)
        else:
            applicant_name = req.POST.get('applicant_name')
            applicant_email = req.POST.get('applicant_email')
            applicant_resume = req.FILES.get('applicant_resume')
            applicant_cover_letter = req.FILES.get('applicant_cover_letter')

            apply_now = ApplyNow(
                user = current_user,
                job = current_job,
                applicant_name = applicant_name,
                applicant_email = applicant_email,
                applicant_resume = applicant_resume,
                applicant_cover_letter = applicant_cover_letter,
            )

            apply_now.save()
            messages.success(req, "Applied for Successfull.")


    context = {
        'data':single_job,
        "already_applied":already_applied
    }
    return render(req, "common/single_view_job.html", context)

def search_job(req):
    query = req.GET.get('search')
    if query:
        job = JobModel.objects.filter(Q(job_title__icontains=query)|Q(job_description__icontains=query)|Q(job_location__icontains=query)|Q(company_name__icontains=query))

    else:
        job = JobModel.objects.none()


    context ={
        'job':job,
        'query':query
    }        

    return render(req, "common/search_job.html", context)


















