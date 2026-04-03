

"""Project5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from application import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main Pages
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='about'),
    path('reg/', views.reg, name='reg'),
    path('records/', views.records, name='records'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('housewife-dashboard/', views.housewife_dashboard, name='housewife_dashboard'),
    
    # CRUD Operations
    path('delete/<int:id>/', views.delete, name='delete'),
    path('edit/<int:id>/', views.edit_record, name='edit_record'),
    path('update/<int:id>/', views.update_record, name='update_record'),
    
    # New Pages for Housewife Portal
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('find-jobs/', views.find_jobs, name='find_jobs'),
    path('services/', views.services, name='services'),
    path('post-job/', views.post_job, name='post_job'),
    path('job-detail/<int:job_id>/', views.job_detail, name='job_detail'),
    path('apply-job/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('request-quote/', views.request_quote, name='request_quote'),
]