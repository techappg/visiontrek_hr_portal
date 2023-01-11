
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.db.models import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# Create your models here.

domain_choices = (
    ("python","python"),
    ("java","java"),
    ("react","react"),
    ("designing","designing"),
    ("Bde","Bde")
)

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
    

class User(AbstractUser):
    first_name = models.CharField(max_length=150,null=True,blank=True)
    last_name = models.CharField(max_length=150,null=True,blank=True)
    fcm_token = models.TextField(default="",null=True,blank=True)
    email = models.EmailField("email address",null=True,blank=True)
    user_type = models.CharField(default="Admin", choices=user_role, max_length=10, null=True, blank=True)
    Employee_code = models.IntegerField(unique=True,null=True,blank=True)
    soft_delete = models.BooleanField(default=False)
    address=models.CharField( max_length=520,null=True,blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=10 , choices= positon_choices,null=True,blank=True)
    domain=models.CharField(max_length=50,choices=domain_choices,null=True, blank=True)
    reporting_to = models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
         return self.username
     
     

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password_token = models.CharField( max_length=520)
    created_at =  models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.user.username

class Reporting(models.Model):
    report_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Reporting_to',null=True,blank=True)
    new_reporting_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name='New_reporting_to',null=True,blank=True)
    report_from = models.DateField(auto_now=False)
    report_till = models.DateField(auto_now=False)
    report_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name='Reporting_by')




# Create your models here.

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        msg_obj = ChatMessage.objects.all().last()
        data = {'count': msg_obj, 'current_txt': self.message}

        (channel_layer.group_send)(
            f'user_chatroom_{msg_obj.thread_id}', {
                'type': 'send_notification',
                'value': json.dumps(msg_obj.message)
            }

        )
        
        super(ChatMessage, self).save(*args,**kwargs)