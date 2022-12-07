from django.urls import path
from . views import *


urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('home/',home,name='home'),
    path('interview_create',create_meeting,name='create_meeting'),
    path('hr_dashboard/',Hr_Dashboard,name='hr_dashboard'),
    path('delete_db',delete_data,name='delete_data'),
    path('delete_db_ofc',delete_data_offc,name='delete_data_offc'),

    path('edit_data',edit_data,name='edit_data'),
    path('selected',selected_data,name='selected'),
    path('rejected',reject_data,name='rejected'),
    path('hold',hold_data,name='hold'),
    path('office_meeting',office_meeting,name='office_meeting'),
    path('office_meeting_data',office_meeting_data,name='office_meeting_data'),
    path('edit_office_meeting',edit_office_meeting,name='edit_offc_data'),
    path('add_student/', AddUser, name="adduser"),
    path('emp_leave_apply/', Empl_leave_apply, name="emp_leave_apply"),





    
    
    
]
