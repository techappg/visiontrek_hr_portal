
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class Domain_name(models.Model):
    name = models.CharField( max_length=25)
    def __str__(self):
        return self.name


user_role  = (
        ("Admin", "Admin"),
        ("HR", 'HR'),
        ("MD", 'MD'),
        ("TL","TL"),
        ("Intern",'Intern'),
        ("Employee", "Employee") )


positon_choices = (
    ("Sr", "Sr"),
    ("Jr", 'Jr'),
    ("Intern", 'Intern'),
    )

class Pos_choice(models.Model):
    position = models.CharField(max_length=50,choices=positon_choices)

    def __str__(self):
        return self.position
    

class User(AbstractUser):
    first_name = models.CharField(max_length=150,null=True,blank=True)
    last_name = models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField("email address",null=True,blank=True)
    
    Employee_code = models.IntegerField(unique=True,null=True,blank=True)
    soft_delete = models.BooleanField(default=False)
    address=models.CharField( max_length=520)
    phone = models.CharField(max_length=100, null=True, blank=True)
    usertype = models.CharField(max_length=10 , choices= user_role)
    position = models.CharField(max_length=10 , choices= positon_choices)
    domain=models.ForeignKey(Domain_name, on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
         return self.username
     
     

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password_token = models.CharField( max_length=520)
    created_at =  models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.user.username