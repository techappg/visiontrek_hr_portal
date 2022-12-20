
from django.db import models
from account.models  import *

status_choices = (
    ("Hold", 'Hold'),
    ("Selected", 'Selected'),
    ("Rejected", 'Rejected'),)

task_choice = (
    ("learning","learning"),
    ("development","development"),
    ("task","task"),
    ("project","project"),
    ("deployment","deployment")
)


class Office_meeting(models.Model):
    Meeting_Agenda=models.CharField( max_length=50)
    Description=models.TextField() 
    datetime= models.DateTimeField( auto_now=False, auto_now_add=False)
    user = models.CharField(max_length=50)
    soft_delete=models.BooleanField(default=False)  #softdelete

    
    
    
class Interview_meeting(models.Model):
    mode = (
        ('Offline','Offline'),
        ('Online','Online')
    )


    first_name=models.CharField(max_length=120,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    user_cv=models.FileField( upload_to='cv/', max_length=100,null=True,blank=True)
    email=models.EmailField( max_length=254)
    phone=models.IntegerField()
    address = models.CharField(max_length=200,null=True,blank=True)
    datetime= models.DateTimeField(auto_now=False, auto_now_add=False,null=True,blank=True)
    user = models.CharField(max_length=100,null=True,blank=True)
    domain_interview=models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=20,null=True,blank=True)
    mode_choice = models.CharField(max_length=50,choices=mode,null=True,blank=True)
    position=models.CharField(max_length=10,choices=positon_choices,null=True,blank=True)
    status=models.CharField(max_length=10,choices=status_choices,default="Hold")
    attempt=models.CharField( max_length=50,null=True,blank=True)
    def __str__(self):
        return self.first_name
    
    
class Punch(models.Model):
    punch_date = models.CharField(max_length=50,null=True,blank=True)
    punch_in = models.TimeField(auto_now=False, auto_now_add=False,null=True,blank=True)
    punch_out = models.TimeField(auto_now=False, auto_now_add=False,null=True,blank=True)
    hours = models.CharField(max_length=100,null=True,blank=True)
    marked=models.BooleanField(default=False,blank=True,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
  
class LeaveReportEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Task(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    task_type = models.CharField(max_length=50,choices=task_choice)
    screenshot = models.ImageField( upload_to='task/',null=True,blank=True)
    detail = models.TextField()

class Project(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    start_date = models.DateField(null=True,blank=True)
    status = models.BooleanField(default=False,null=True,blank=True)
    detail = models.TextField(max_length=200,null=True,blank=True)



class NotificationEmp(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    