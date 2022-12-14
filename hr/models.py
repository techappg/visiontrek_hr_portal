
from django.db import models
from account.models  import *

status_choices = (
    ("Hold", 'Hold'),
    ("Selected", 'Selected'),
    ("Rejected", 'Rejected'),)




class Office_meeting(models.Model):
    Meeting_Agenda=models.CharField( max_length=50)
    Description=models.TextField() 
    datetime= models.DateTimeField( auto_now=False, auto_now_add=False)
    user = models.ManyToManyField(User, related_name='user_office_meeting' )
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
    
    
  