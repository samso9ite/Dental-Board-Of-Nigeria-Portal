from django.db import models
from authentication.models import User
from schPortal.models import *

# Create your models here.


class IndexLimit(models.Model):
    school = models.CharField(max_length=10)
    assigned_limit = models.CharField(max_length=40)
    year = models.CharField(max_length=10, blank=True, null=True) 
  
    def __str__(self):
        return self.assigned_limit


class examLimit(models.Model):
    school = models.CharField(max_length=10)
    assigned_limit = models.CharField(max_length=40)
    year = models.CharField(max_length=10, blank=True, null=True) 
  
    def __str__(self):
        return self.assigned_limit

class Restrictions(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.BooleanField(default=False)
    suspend = models.BooleanField(default=False)

class closeIndexing(models.Model):
    access = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

class closeExamRegistration(models.Model):
    access = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    