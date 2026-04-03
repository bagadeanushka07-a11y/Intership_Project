from django.shortcuts import render, redirect, HttpResponseRedirect
from application.models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

def home(request):
    # Get latest jobs for homepage
    latest_jobs = JobPost.objects.all().order_by('-created_at')[:3]
    top_freelancers = User.objects.filter(groups__name='housewife')[:4]  # Assuming housewife group exists
    
    context = {
        'latest_jobs': latest_jobs,
        'top_freelancers': top_freelancers,
    }
    return render(request, 'index.html', context)

def aboutus(request):
    return render(request, 'about.html')

def how_it_works(request):
    return render(request, 'how_it_works.html')

def find_jobs(request):
    # Get all active jobs
    jobs = JobPost.objects.filter(is_active=True).order_by('-created_at')
    
    # Filter by category if selected
    category = request.GET.get('category')
    if category:
        jobs = jobs.filter(category=category)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    context = {'jobs': jobs}
    return render(request, 'find_jobs.html', context)

def post_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        description = request.POST.get('description')
        budget = request.POST.get('budget')
        location = request.POST.get('location')
        
        job = JobPost(
            title=title,
            category=category,
            description=description,
            budget=budget,
            location=location,
            posted_by=request.user if request.user.is_authenticated else None,
            is_active=True
        )
        job.save()
        messages.success(request, 'Job posted successfully!')
        return redirect('find_jobs')
    
    return render(request, 'post_job.html')

def services(request):
    return render(request, 'services.html')

def reg(request):
    if request.method == 'POST':
        a = request.POST.get('name')
        b = request.POST.get('email')
        c = request.POST.get('phone')
        d = request.POST.get('message')
        user_type = request.POST.get('user_type')  # 'housewife' or 'client'
        password = request.POST.get('password')  # Get password from form
        confirm_password = request.POST.get('confirm_password')  # Get confirm password

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'reg.html')

        # Check password length
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long!')
            return render(request, 'reg.html')

        # Check if user already exists
        if User.objects.filter(email=b).exists():
            messages.error(request, 'Email already registered! Please login.')
            return render(request, 'reg.html')
        
        # Create username from email
        username = b.split('@')[0]
        
        # Check if username already exists, if yes add number
        if User.objects.filter(username=username).exists():
            username = username + str(User.objects.count())
        
        # Create user account with the password from form
        user = User.objects.create_user(username=username, email=b, password=password)
        user.save()
        
        # Save enquiry
        info = enquiry_table(name=a, email=b, phone=c, message=d)
        info.save()
        
        # Create user profile
        profile = UserProfile(user=user, user_type=user_type, phone=c)
        profile.save()
        
        messages.success(request, 'Registration successful! Please login with your email and password.')
        return redirect('login')
    
    return render(request, 'reg.html')

def records(request):
    info = enquiry_table.objects.all()
    dict1 = {'abc': info}
    return render(request, 'records.html', dict1)

def login_user(request):
    if request.method == 'POST':
        a = request.POST.get('username')
        b = request.POST.get('password')

        # Try to find user by email first
        try:
            user_obj = User.objects.get(email=a)
            username = user_obj.username
        except User.DoesNotExist:
            username = a  # Use as username if not found as email

        user = authenticate(request, username=username, password=b)

        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            
            # Check user type and redirect accordingly
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.user_type == 'housewife':
                    return redirect('housewife_dashboard')
                else:
                    return redirect('dashboard')
            except UserProfile.DoesNotExist:
                return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect username/email or password')

    return render(request, 'login.html')

@login_required(login_url='login')
def dashboard(request):
    username = request.session.get('username')
    
    # Get user's posted jobs
    my_jobs = JobPost.objects.filter(posted_by=request.user)
    
    # Get job applications for user
    applications = JobApplication.objects.filter(freelancer=request.user)
    
    context = {
        'username': username,
        'my_jobs': my_jobs,
        'applications': applications,
    }
    return render(request, 'dashboard/index.html', context)

@login_required(login_url='login')
def housewife_dashboard(request):
    username = request.session.get('username')
    
    # Get jobs applied by this housewife
    applied_jobs = JobApplication.objects.filter(freelancer=request.user)
    
    # Get available jobs
    available_jobs = JobPost.objects.filter(is_active=True).exclude(
        id__in=applied_jobs.values_list('job_id', flat=True)
    )[:10]
    
    # Get earnings
    completed_jobs = JobApplication.objects.filter(
        freelancer=request.user, 
        status='completed'
    )
    total_earnings = 0
    for job in completed_jobs:
        if job.amount:
            try:
                # Extract number from amount string (e.g., "₹300-500" -> 300)
                amount_str = str(job.amount).replace('₹', '').split('-')[0].strip()
                total_earnings += int(amount_str) if amount_str.isdigit() else 0
            except:
                pass
    
    context = {
        'username': username,
        'applied_jobs': applied_jobs,
        'available_jobs': available_jobs,
        'total_earnings': total_earnings,
        'completed_count': completed_jobs.count(),
    }
    return render(request, 'dashboard/housewife_dashboard.html', context)

@login_required(login_url='login')
def apply_for_job(request, job_id):
    job = JobPost.objects.get(id=job_id)
    
    # Check if already applied
    existing = JobApplication.objects.filter(job=job, freelancer=request.user).first()
    if existing:
        messages.warning(request, 'You have already applied for this job!')
    else:
        application = JobApplication(
            job=job,
            freelancer=request.user,
            status='pending',
            amount=job.budget
        )
        application.save()
        messages.success(request, 'Application submitted successfully!')
    
    return redirect('find_jobs')

@login_required(login_url='login')
def job_detail(request, job_id):
    job = JobPost.objects.get(id=job_id)
    has_applied = JobApplication.objects.filter(job=job, freelancer=request.user).exists()
    
    context = {
        'job': job,
        'has_applied': has_applied,
    }
    return render(request, 'job_detail.html', context)

@login_required(login_url='login')
def records_list(request):
    info = enquiry_table.objects.all()
    dict1 = {'records': info}
    return render(request, 'dashboard/tables.html', dict1)

def delete(request, id):
    if request.method == 'POST':
        data = enquiry_table.objects.get(pk=id)
        data.delete()
    return HttpResponseRedirect('/records/')

@login_required(login_url='login')
def edit_record(request, id):
    info = enquiry_table.objects.filter(pk=id)
    data = {'information': info}
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

def request_quote(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service_type = request.POST.get('service_type')
        message = request.POST.get('message')
        
        # Save quote request
        quote = ServiceRequest(
            name=name,
            email=email,
            phone=phone,
            service_type=service_type,
            message=message
        )
        quote.save()
        
        messages.success(request, 'Your request has been sent! We will contact you soon.')
        return redirect('home')
    
    return redirect('home')