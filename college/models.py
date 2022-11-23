from django.db import models
from django.contrib.auth.models import User

# Create your models here.

faculties = [('BSc. CSIT', 'BSc. CSIT'),('BIT','BIT'),('BSc.','BSc.'),('MSc.','MSc.')]
class Student(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    roll= models.CharField(max_length=10)
    phone_no = models.CharField(max_length=50,blank=True)
    address = models.CharField(max_length=200, blank=True)
    faculty= models.CharField(max_length=10,choices=faculties,default='Bsc. CSIT')
    fee=models.PositiveIntegerField(blank=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.first_name
    
    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name
    
    @property
    def get_id(self):
        return self.user.id
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salary= models.PositiveIntegerField(blank=False)
    joindate = models.DateField(auto_now_add=True)
    phone_no = models.CharField(max_length=50,blank=True)
    address = models.CharField(max_length=200, blank=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.first_name 
    
    @property
    def get_id(self):
        return self.user.id
    
    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name
    

class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,blank=True,default='college')
    topic = models.CharField(max_length=100,blank=True)
    message=models.CharField(max_length=600)


class Attendance(models.Model):
    faculty = models.CharField(max_length=10)
    roll = models.CharField(max_length=10, blank=True)
    present = models.CharField(max_length=10)
    date = models.DateField()
    
    
class Complain(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,blank=True,default='college')
    topic = models.CharField(max_length=100,blank=True)
    message=models.CharField(max_length=600)
    
    
class Leave(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,blank=True,default='college')
    topic = models.CharField(max_length=100,blank=True)
    message=models.CharField(max_length=700)

