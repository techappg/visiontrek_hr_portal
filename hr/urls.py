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
    path('total_candidate',total_candidate,name='total_candidate'),
    path('hold',hold_data,name='hold'),
    path('office_meeting',office_meeting,name='office_meeting'),
    path('office_meeting_data',office_meeting_data,name='office_meeting_data'),
    path('edit_office_meeting',edit_office_meeting,name='edit_offc_data'),
    path('add_student/', AddUser, name="adduser"),
    path('emp_leave_apply/', Empl_leave_apply, name="emp_leave_apply"),
    path('add_task/', add_task, name="add_task"),
    path('hr_leave_view/', hr_leave_view, name="hr_leave_view"),
    path('emp_leave_view/', emp_leave_view, name="emp_leave_view"),
    path('python_team/<status>', python_team, name="python_team"),
    path('emp_leave_views/<status>', emp_leave_views, name="emp_leave_views"),
    path('emp_task_view/', emp_task_view, name="emp_task_view"),
    path('emp_leave_approve/<leave_id>/', emp_leave_approve, name="emp_leave_approve"),
    path('emp_leave_reject/<leave_id>/', emp_leave_reject, name="emp_leave_reject"),
    path('add_project/', add_project, name="add_project"),
    path('show_project/', show_project, name="show_project"),
    path('active_project/', active_project, name="active_project"),
    path('complete_project/', complete_project, name="complete_project"),
    path('reporting_hr/', reporting_hr, name="reporting_hr"),
    path('report_by_hr/', report_by_hr, name="report_by_hr"),


]
