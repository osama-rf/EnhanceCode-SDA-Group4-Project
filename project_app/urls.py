"""Group4_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [

    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('home',views.home),
    path('logout',views.logout),
    path('show/<course_id>',views.show_course),
    path('show/subject/<subject_id>',views.show_subject),



    path('dashboard',views.dashboard),
    path('dashboard/category',views.all_categories),
    path('dashboard/category/new',views.new_category),
    path('dashboard/category/create',views.create_category),
    path('dashboard/category/edit/<category_id>',views.edit_category),
    path('dashboard/category/update/<category_id>',views.update_category),
    path('dashboard/category/delete/<category_id>',views.delete_category),


    path('dashboard/course',views.all_courses),
    path('dashboard/course/new',views.new_course),
    path('dashboard/course/create',views.create_course),
    path('dashboard/course/edit/<course_id>',views.edit_course),
    path('dashboard/course/update/<course_id>',views.update_course),
    path('dashboard/course/delete/<course_id>',views.delete_course),


    path('dashboard/section',views.all_sections),
    path('dashboard/section/new',views.new_section),
    path('dashboard/section/create',views.create_section),
    path('dashboard/section/edit/<section_id>',views.edit_section),
    path('dashboard/section/update/<section_id>',views.update_section),
    path('dashboard/section/delete/<section_id>',views.delete_section),



    path('dashboard/subject',views.all_subjects),
    path('dashboard/subject/new',views.new_subject),
    path('dashboard/subject/create',views.create_subject),
    path('dashboard/subject/edit/<subject_id>',views.edit_subject),
    path('dashboard/subject/update/<subject_id>',views.update_subject),
    path('dashboard/subject/delete/<subject_id>',views.delete_subject),
    
]
