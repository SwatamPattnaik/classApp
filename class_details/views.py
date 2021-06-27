from django.shortcuts import render
from django.urls import reverse

from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound

from django.contrib.auth import logout,login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from .forms import *
from .models import *

import json,sys

from datetime import *
# Create your views here.

def redirect_url(request):
    return HttpResponseRedirect(reverse('class_details:index'))

def index(request):
    try:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        if request.user.is_authenticated and request.user.is_staff:
            return HttpResponseRedirect(reverse('class_details:admin'))
        
        user_details = request.user
        student_details = Student.objects.get(user_id=user_details.id)
        return render(request, 'class_details/index.html',{'student':student_details})
    except:
        return HttpResponseNotFound()

def user_login(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        login_valid = True if user.exists() else False
        pwd_valid = check_password(password, user[0].password)
        if login_valid and pwd_valid:
            if user[0].is_staff:
                login(request, user[0])
                return HttpResponse(status=204)
            student = Student.objects.get(user_id=user[0].id)
            if student and student.status==1:
                login(request, user[0])
                return HttpResponse(status=204)
            else:
                return HttpResponse("Account not activated.Please contact admin.",status="400")
        else:
            return HttpResponse("Username Password does not match.",status="400")
    except:
        return HttpResponse('Something went wrong.Please try again later.', status="400")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def user_registration(request):
    try:
        if request.method == 'POST':
            form = RegistrationForm(request.POST,request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                first_name = cd.get('first_name')
                last_name = cd.get('last_name')
                dob = cd.get('dob')
                email = cd.get('email')
                password = cd.get('password2')
                image = cd.get('image')
                class_id = cd.get('class_id')
                class_obj = Class.objects.get(id=class_id)
                status = 0
                user = User.objects.create_user(email,email,password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                student = Student.objects.create(user_id=user.id,first_name=first_name,last_name=last_name,dob=dob,email=email,status=status,class_field=class_obj,image=image)
                student.image = student.image.name.split('/')[-1]
                student.save()
                return HttpResponseRedirect(reverse('class_details:index'))
            else:
                return render(request, 'class_details/user_registration_form.html', {'form': form})
        else:
            form = RegistrationForm()
            return render(request, 'class_details/user_registration_form.html', {'form': form})
    except:
        return HttpResponseRedirect(reverse('class_details:index'))

def admin(request):
    try:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        if request.user.is_authenticated and not request.user.is_staff:
            return HttpResponseRedirect(reverse('class_details:index'))
        classes = Class.objects.all()
        students = Student.objects.all().order_by('class_field')
        return render(request, 'class_details/admin.html',{'classes':classes,'students':students})
    except:
        return HttpResponseRedirect(reverse('class_details:index'))

def update_status(request):
    try:
        student_id = request.POST.get('student_id')
        status = request.POST.get('status')
        Student.objects.filter(id=student_id).update(status=status)
        return HttpResponse(status=204)
    except:
        return HttpResponse('Something went wrong.Please try again later.', status=200)

def add_class(request):
    try:
        class_name = request.POST.get('class_name')
        if Class.objects.filter(name=class_name).exists():
            return HttpResponse('Class exists already!',status=200)
        Class.objects.create(name=class_name)
        return HttpResponse(status=204)
    except:
        return HttpResponse('Something went wrong.Please try again later.', status=200)

def student_form(request,student_id):
    try:
        student = Student.objects.get(id=student_id)
        if request.method == 'POST':
            form = StudentForm(student_id,request.POST,request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                first_name = cd.get('first_name')
                last_name = cd.get('last_name')
                dob = cd.get('dob')
                email = cd.get('email')
                image = cd.get('image')
                class_field = cd.get('class_field')
                Student.objects.filter(id=student_id).update(first_name=first_name,last_name=last_name,dob=dob,email=email,image=image,class_field=class_field)
                student = Student.objects.get(id=student_id)
                return render(request, 'class_details/index.html',{'student':student})
            else:
                return render(request,'class_details/student_form.html',{'form':form,'student':student})
        else:
            form = StudentForm(student_id)
            return render(request, 'class_details/student_form.html', {'form': form,'student':student})
    except:
        return HttpResponse('Something went wrong.Please try again later.', status=200)
