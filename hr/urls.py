from django.urls import path
from . views import *


urlpatterns = [
    path('',dashboard,name='dashboard'),
    path('home/',home,name='home'),
    path('interview_create',create_meeting,name='create_meeting'),
    path('hr_dashboard/',Hr_Dashboard,name='hr_dashboard'),
    path('delete_db',delete_data,name='delete_data'),
    path('edit_data',edit_data,name='edit_data'),
    path('selected',selected_data,name='selected'),
    path('rejected',reject_data,name='rejected'),
    path('hold',hold_data,name='hold')
    
    
    
]
