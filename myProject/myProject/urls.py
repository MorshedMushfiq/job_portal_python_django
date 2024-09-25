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
    path('add_basic_info/', add_basic_info, name='add_basic_info'),
    path('edit_basic_info/<int:id>', edit_basic_info, name='edit_basic_info'),

    path('add_skills/', add_skills, name='add_skills'),
    path('add_basic_info/', add_basic_info, name='add_basic_info'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


