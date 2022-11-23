from django.contrib import admin
from . models import *
from hr.models import *
# Register your models here.



admin.site.register([User,Domain_name,Pos_choice,Profile,Interview_meeting,Office_meeting])