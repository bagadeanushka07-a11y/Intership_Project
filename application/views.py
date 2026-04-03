from django.shortcuts import render, redirect, HttpResponseRedirect
from application.models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):

    return render(request, 'index.html')

def aboutus(request):

    return render(request, 'about.html')

def reg(request):

    if request.method=='POST':
        a = request.POST.get('name')
        b = request.POST.get('email')
        c = request.POST.get('phone')
        d = request.POST.get('message')

        info = enquiry_table(name = a, email = b, phone = c, message = d)
        info.save()
        messages.success(request, 'Enquiry form has been sent successful..')

    return render(request, 'reg.html')

def records(request):

    info = enquiry_table.objects.all()

    dict1 = {'abc':info}

    return render(request, 'records.html', dict1)

def login_user(request):

    if request.method=='POST':
        a = request.POST.get('username')
        b = request.POST.get('password')

        user = authenticate(request, username = a, password = b)

        if user is not None:
            login(request, user)
            request.session['username'] = a
            return redirect('dashboard')
        else:
            messages.error(request, 'incorrect username or password')

    return render(request, 'login.html')

@login_required(login_url='login')
def dashboard(request):

    username = request.session.get('username')

    return render(request, 'dashboard/index.html',{'username':username})

@login_required(login_url='login')
def records(request):

    info = enquiry_table.objects.all()

    dict1 = {'records':info}

    return render(request, 'dashboard/tables.html',dict1)

def delete(request, id):
    if request.method=='POST':

        data = enquiry_table.objects.get(pk=id)
        data.delete()

    return HttpResponseRedirect('/records/')

@login_required(login_url='login')
def edit_record(request, id):
    info = enquiry_table.objects.filter(pk=id)
    
    data = {'information':info}
    return render(request, 'dashboard/editrecord.html', data)

def update_record(request, id):
    info = enquiry_table.objects.get(pk=id)
    
    info.name = request.POST.get('name')
    info.email = request.POST.get('email')
    info.phone = request.POST.get('phone')
    info.message = request.POST.get('message')
    info.save()

    return HttpResponseRedirect('/records/')

def logout_user(request):

    logout(request)
    return redirect('/')



