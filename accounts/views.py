import email
import profile
from re import template
from django.shortcuts import render, redirect
from flask import render_template, render_template_string
from .models import Project
from django.shortcuts import get_object_or_404
from .models import *
from .forms import ProjectForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

# views


from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            print('Printing post:', request.POST)
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()

                fname = form.cleaned_data.get('first_name')
                reg_email = form.cleaned_data.get('email')
                reg_username = form.cleaned_data.get('username')
                messages.success(request, 'Account created. Welcome, ' + fname + '!')

                # send mail to confirm the user of his successful registration
                template = render_to_string('accounts/onboard.html', {'fname':fname, 'reg_email':reg_email, 'reg_username':reg_username})
                
                # from templated_email import get_templated_mail

                # get_templated_mail(
                #     template_name='Welcome aboard' + ' ' + fname + '!',
                #     from_email=settings.EMAIL_HOST_USER,
                #     to=[reg_email],
                #     context={
                #         'reg_username':request.user.username,
                #         'fname':request.user.first_name,
                #         'reg_email':request.user.email
                #     },
                #     # Optional:
                #     # cc=['cc@example.com'],
                #     # bcc=['bcc@example.com'],
                #     # headers={'My-Custom-Header':'Custom Value'},
                #     # template_prefix="my_emails/",
                #     # template_suffix="email",
                # )

                email = EmailMessage(
                    'Welcome aboard' + ' ' + fname + '!',
                    template,
                    settings.EMAIL_HOST_USER,
                    [reg_email],
                )

                email.fail_silently = False
                email.send()

                return redirect('login')

    

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def confirmLogout(request):
    return render(request, 'prompt/logoutUser.html')

@login_required(login_url='login')
def dashboard(request):
    projects = Project.objects.all()
    return render(request, 'accounts/dashboard.html', {'projects':projects})

def status(request, no):
    projects = get_object_or_404(Project, pk=no) 
    return render(request, 'accounts/status.html',{'projects':projects})

@login_required(login_url='login')
def addProject(request): 
    form = ProjectForm()
    if request.method == 'POST':
        # print('printing post:', request.POST)
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('/dashboard')

            return render(request, 'messages/projectAdded.html')

    context = {'form':form}
    return render(request, 'forms/addProject.html', context)

@login_required(login_url='login')
def updateProject(request, no):
    proj = Project.objects.get(id=no)
    form  = ProjectForm(instance=proj)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=proj)
        if form.is_valid():
            form.save()
            # return redirect('/dashboard')
            return render(request, 'messages/projectUpdated.html')
    
    context = {'form':form}
    return render(request, 'forms/updateProject.html', context)

@login_required(login_url='login')
def deleteProject(request, no):
    proj = Project.objects.get(id=no)

    if request.method == 'POST':
        proj.delete()
        return redirect('/dashboard')


    context = {'item':proj}
    return render(request, 'prompt/deleteProject.html', context)