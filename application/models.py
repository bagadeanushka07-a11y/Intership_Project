from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class enquiry_table(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return self.name


# New Models for Freelancer Housewife Portal

class JobPost(models.Model):
    CATEGORY_CHOICES = [
        ('cooking', '🍳 Cooking'),
        ('cleaning', '🧹 Home Cleaning'),
        ('tutoring', '📚 Tutoring'),
        ('beauty', '💄 Beauty Services'),
        ('childcare', '👶 Childcare'),
        ('craft', '🎨 Craft & Handmade'),
        ('baking', '🎂 Baking'),
        ('digital', '💻 Digital Services'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    budget = models.CharField(max_length=100, help_text="e.g., ₹300-500/day or ₹5000/month")
    location = models.CharField(max_length=200)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', '⏳ Pending'),
        ('accepted', '✅ Accepted'),
        ('rejected', '❌ Rejected'),
        ('completed', '🎉 Completed'),
    ]
    
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.CharField(max_length=100, blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.freelancer.username} - {self.job.title}"


class ServiceRequest(models.Model):
    SERVICE_CHOICES = [
        ('cooking', '🍳 Cooking'),
        ('cleaning', '🧹 Home Cleaning'),
        ('tutoring', '📚 Tutoring'),
        ('craft', '🎨 Craft & Handmade'),
        ('beauty', '💄 Beauty Services'),
        ('childcare', '👶 Childcare'),
        ('baking', '🎂 Baking'),
        ('digital', '💻 Digital Services'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('housewife', '👩‍🍳 Housewife Freelancer'),
        ('client', '👔 Client'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='client')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="List your skills (for housewives)")
    experience = models.TextField(blank=True, help_text="Your experience (for housewives)")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"