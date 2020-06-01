from django.db import models
from django.contrib.auth.models import AbstractUser
# from authentication.choices import *
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(AbstractUser):
    cadre_choices = (
        ('Dental Therapist', 'Dental Therapist'),
        ('Dental Surgery Technician', 'Dental Surgery Technician'),
        ('Dental Surgery Assistant', 'Dental Surgery Assistant'),
        ('Dental Nurses', 'Dental Nurses'),
    ) 
    username = models.CharField(max_length=200, unique=True,null=True)
    code = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    programme = models.CharField(max_length=100, null=True)
    school_logo = models.FileField(upload_to='images/school/sch_logo', null=True)
    reset = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_school = models.BooleanField(default=False, blank=True)
    is_professional = models.BooleanField(default=False, blank=True)
    profile_update = models.BooleanField(default=False, blank=True)
    block = models.BooleanField(default=False)
    suspend = models.BooleanField(default=False)
   

class Professional(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=300, blank=True)
    middle_name = models.CharField(max_length=300, blank=True)
    last_name = models.CharField(max_length=300, blank=True)
    licence_due_date = models.DateField()


class SchoolCode(models.Model):
    reg_number = models.CharField(max_length=50)
    used = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class ProfessionalCode(models.Model):
    reg_number = models.CharField(max_length=50)
    used = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cadre = models.CharField(max_length=30, null=True)
    

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    ticket_status = models.CharField(max_length=20)
    message = models.CharField(max_length=500)
    department = models.CharField(max_length=50)
    priority = models.CharField(max_length=20)
    attachment1 = models.FileField(upload_to='images/ticket_attachments', null=True, blank=True)
    attachment2 = models.FileField(upload_to='images/ticket_attachments', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add = True)
    last_updated = models.DateTimeField(blank=True, null=True, auto_now_add = True)
    subject = models.CharField(max_length=200)
    ticket_id = models.IntegerField(null=True)
    first_created = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)


class SubTicket(models.Model):
    parent_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='parent_ticket')
    attachment1 = models.FileField(upload_to='images/ticket_attachments', null=True, blank=True)
    attachment2 = models.FileField(upload_to='images/ticket_attachments', null=True, blank=True)
    message = models.CharField(max_length=500)
    ticket_status = models.CharField(max_length=20)
   









