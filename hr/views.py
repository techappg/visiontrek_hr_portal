from django.shortcuts import render, redirect
from . models import *
from account.models import *
from django.db.models import Q
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives,send_mail,EmailMessage
from django.contrib.auth.hashers import make_password

from datetime import datetime, date
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import HttpResponse
from . models import task_choice
import json
from django.contrib.auth.models import User
from account.models import domain_choices,user_role,positon_choices
from django.contrib.auth import get_user_model
from datetime import timedelta

# Create your views here.
User = get_user_model()



def hr_leave_view(request):
    try:
        leaves = LeaveReportEmployee.objects.all()
        context = {
            "leaves": leaves
        }
        return render(request,'emp_leave_view.html',context)
    except:
        messages.error(request, "error occur")
        return render(request,'emp_leave_view.html')


def Empl_leave_apply(request):
    try:
        user_obj = User.objects.get(username=request.user)
        leave_obj = LeaveReportEmployee.objects.filter(emp_id=user_obj)
        if request.method == "POST":
            leave_date = request.POST.get('leave_date')
            leave_message = request.POST.get('leave_message')

            emp_obj = User.objects.get(id=request.user.id)
            
            leave_report = LeaveReportEmployee(emp_id=emp_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('emp_leave_apply')

        return render(request,'employee/emp_apply_leave.html',{'leaves':leave_obj})
    except:
        messages.error(request, "error occur")
        return render(request,'employee/emp_apply_leave.html')


def emp_leave_views(request, status):
    try:
        user_obj = User.objects.get(username=request.user)
        leave_obj = LeaveReportEmployee.objects.filter(emp_id=user_obj, leave_status=status)
        return render(request,'employee/emp_leave_view.html',{'leaves':leave_obj})
    except:
        messages.error(request, "error occur")
        return render(request,'employee/emp_leave_view.html')


def python_team(request,status):
    try:
        user_obj = User.objects.filter(domain=status)
        return render(request,'employee/python_team.html',{'user':user_obj})
    except:
        messages.error(request, "error occur")
        return render(request,'employee/python_team.html')


def emp_leave_view(request):
    try:   
        user_obj = User.objects.get(username=request.user)
        leave_obj = LeaveReportEmployee.objects.filter(emp_id=user_obj)
        return render(request,'employee/emp_leave_view.html',{'leaves':leave_obj})
    except:
        messages.error(request, "error occur")
        return render(request,'employee/emp_leave_view.html')


def emp_leave_approve(request, leave_id):
    try:
        leave = LeaveReportEmployee.objects.get(id=leave_id)
        leave.leave_status = 1
        leave.save()
        return redirect('hr_leave_view')
    except:
        messages.error(request, "error occur")
        return redirect('hr_leave_view')


def emp_leave_reject(request, leave_id):
    try:
        leave = LeaveReportEmployee.objects.get(id=leave_id)
        leave.leave_status = 2
        leave.save()
        return redirect('hr_leave_view')
    except:
        messages.error(request, "error occur")
        return redirect('hr_leave_view')


def emp_task_view(request):
    try:
        task_obj = Task.objects.filter(user_id=request.user.id)
        date_obj = date.today()
        context = {
            "task":task_obj,
            'date':date_obj
        }
        return render(request,'employee/show_task.html',context)
    except:
        messages.error(request, "error occur")
        return render(request,'employee/show_task.html')


def dashboard(request):
    return render(request,'employee/base.html')

def show_attendence(request):
    punch = Punch.objects.filter(user=request.user)
    punch_obj = Punch.objects.filter(user=request.user).last()
    if punch_obj!= None:
        a = punch_obj.marked
        b = punch_obj.punch_out
        c = punch_obj.punch_in
        if b!= None:
            d =datetime.combine(date.today(), b) - datetime.combine(date.today(), c)

            
            punch_obj.hours = d
            punch_obj.save()
        else:
            d = None
        context = { 
            'punch':punch,
            'mark':a,
            'out':d
           
        }
        
    
    return render(request,'employee/show_attendence.html',context)
    
def report_by_hr(request):
    return render(request,'report_by.html')
def report_to_hr(request):
    try:
        user_obj = User.objects.get(id=request.user.id)
        report_to_user = user_obj.reporting_to
        emp = User.objects.get(username=report_to_user)
        return render(request,'report_to.html',{'emp':emp})

    except :
        return render(request,'report_to.html')
def reporting_hr(request):
    try:

        return render(request,'manage_reporting.html')
    except Exception as e:
        return render(request,'manage_reporting.html')

def employee_home(request):
    try:
        obj_id = request.user.id
        punch = Punch.objects.filter(user=request.user)
        project_count = Project.objects.filter(user_id=obj_id).count()
        task_count = Task.objects.filter(user_id=obj_id).count()
        attendence_count = Punch.objects.filter(user_id=obj_id).count()
        pending_leave_count = LeaveReportEmployee.objects.filter(emp_id=obj_id, leave_status=0).count()
        reject_leave_count = LeaveReportEmployee.objects.filter(emp_id=obj_id, leave_status=2).count()
        accept_leave_count = LeaveReportEmployee.objects.filter(emp_id=obj_id, leave_status=1).count()

        punch_obj = Punch.objects.filter(user=request.user).last()
        context = { 
                'project_count':project_count,
                'task_count':task_count,
                'attendence_count':attendence_count,
                'pending_leave_count':pending_leave_count,
                'reject_leave_count':reject_leave_count,
                'accept_leave_count':accept_leave_count
            }
        if punch_obj!= None:
            a = punch_obj.marked
            b = punch_obj.punch_out
            c = punch_obj.punch_in
            if b!= None:
                d =datetime.combine(date.today(), b) - datetime.combine(date.today(), c)

                
                punch_obj.hours = d
                punch_obj.save()
            else:
                d = None
            context = { 
                'punch':punch,
                'mark':a,
                'out':d,
                'project_count':project_count,
                'task_count':task_count,
                'attendence_count':attendence_count,
                'pending_leave_count':pending_leave_count,
                'reject_leave_count':reject_leave_count,
                'accept_leave_count':accept_leave_count
            }
            
            return render(request,'employee/emp_dashboard.html',context)
        return render(request,'employee/emp_dashboard.html',context)
    except:
        messages.error(request,'error occur')
        return render(request,'employee/emp_dashboard.html')

def add_task(request):
    try:
        if request.method=="POST":
    
            task = request.POST.get("task_val")
            file = request.FILES.get('imagesfiles')
            detail = request.POST.get("taskdetail")
            a = date.today()
            task_obj = Task.objects.create(task_type=task,screenshot=file,detail=detail,user_id=request.user,create_task_date=date.today())
        
        return render(request,'employee/add_task.html',{"choice":dict(task_choice)})
    except:
        messages.error(request,'error occur')
        return render(request,'employee/add_task.html')

def AddUser(request):
    try:
        user_obj = User.objects.all()
        context = {
            "users":user_obj,
            "domain":dict(domain_choices),
            "user_role":dict(user_role),
            "position_choices":dict(positon_choices)
        }
        if request.method == "POST":
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            uname = request.POST.get("uname")
            pswrd = request.POST.get("pwd")
            email = request.POST.get("email")
            utype = request.POST.get("user_id")
            position = request.POST.get("position")
            domain_id = request.POST.get("domain")
            report_to = request.POST.get("report_to")
            phone = request.POST.get("phone")
            user_obj = User.objects.create(first_name=fname,last_name=lname,username=uname,phone=phone,password=make_password(pswrd),email=email,user_type=utype,position=position,domain=domain_id,reporting_to=report_to)
            messages.success(request,'User Added Successfully')
        return render(request,'adduser.html',context)
    except:
        messages.error(request,'add user failled!!')
        return render(request,'adduser.html')




def home(request):
    try:
        all_candidate_count = Interview_meeting.objects.all().count()
        select_count = Interview_meeting.objects.filter(status='Selected').count()
        reject_count = Interview_meeting.objects.filter(status='Rejected').count()
        hold_count = Interview_meeting.objects.filter(status='Hold').count()


        interview_meeting_obj = Interview_meeting.objects.all()
        if request.method == 'POST':
            id = request.GET.get("id")
            user_obj = Interview_meeting.objects.get(id=id)
            status = request.POST['status_id']
            user_obj.status = status
            user_obj.save()


        context = {
            "candidate":interview_meeting_obj,
            "count_candidate":all_candidate_count,
            "select_count":select_count,
            "reject_count":reject_count,
            "hold_count": hold_count
        }

        return render(request,'home.html', context)
    except:
        messages.error(request,'error occur')
        return render(request,'home.html')


def office_meeting(request):
    try:
        user_obj = User.objects.all()
        context = {
            'particepant':user_obj
        } 
        if request.method == "POST":
            agenda = request.POST.get('magenda')
            date = request.POST.get('datetime')
            description = request.POST.get('description')
            participants = request.POST.getlist('user')
            meeting = Office_meeting.objects.create(Meeting_Agenda=agenda,datetime=date,Description=description,user=participants)
            messages.success(request,"Office meeting created  Successfully")

        return render(request,'office_meeting.html',context)
    except:
        messages.error(request,'error occur')
        return render(request,'office_meeting.html')


def office_meeting_data(request):
    try:
        office_obj = Office_meeting.objects.all()
        user_obj = User.objects.all()
        
        context = {
            'office':office_obj,
            'user':user_obj
        }
        return render(request,'office_data.html',context)
    except:
        messages.error(request,'error occur')
        return render(request,'office_data.html')


def delete_data_offc(request):
    try:
        id = request.GET.get("id")
        user = Office_meeting.objects.get(id=id)
        user.delete()
        messages.success(request,"Delete Data Successfully")
        return redirect('office_meeting_data')
    except:
        messages.error(request,'error occur')
        return redirect('office_meeting_data')


def edit_office_meeting(request):
    try:
        id = request.GET.get("id")
        office_obj = Office_meeting.objects.get(id=id)
        user_obj = User.objects.all()
        context = {
            'office':office_obj,
            'user':user_obj
        }
        if request.method == 'POST':
            agenda = request.POST.get('magenda')
            date = request.POST.get('datetime')
            description = request.POST.get('description')
            participants = request.POST.getlist('user')
            office_obj.Meeting_Agenda = agenda
            office_obj.datetime = date
            office_obj.Description = description
            office_obj.user = participants
            office_obj.save()
            messages.success(request,"meeting update successfully")
            return redirect('office_meeting_data')
        return render(request,'edit_offc_data.html',context)
    except:
        messages.error(request,'error occur')
        return render(request,'edit_offc_data.html')

def total_candidate(request):
    try:
        interview_obj = Interview_meeting.objects.all()
        return render(request,'total_candidate.html',{'candidate':interview_obj})
    except:
        messages.error(request,'error occur')
        return render(request,'total_candidate.html')

def selected_data(request):
    try:
        select = Interview_meeting.objects.filter(status='Selected')
        return render(request,'select.html',{'select':select})
    except:
        messages.error(request,'error occur')
        return render(request,'select.html')
    
def reject_data(request):  
    try:
        reject = Interview_meeting.objects.filter(status='Rejected')
        return render(request,'reject.html',{'reject':reject})
    except:
        messages.error(request,'error occur')
        return render(request,'reject.html')

def hold_data(request):
    try:
        hold = Interview_meeting.objects.filter(status='Hold')
        if request.method == 'POST':
            id = request.GET.get("id")
            user_obj = Interview_meeting.objects.get(id=id)
            status = request.POST['status_id']
            user_obj.status = status
            user_obj.save()
        context = {
        'hold': hold,

        }
        return render(request,'hold.html',{'hold':hold})
    except:
        messages.error(request,'error occur')
        return render(request,'hold.html')


def create_meeting(request):
    try:
        user_obj = User.objects.all()
        context = {
            "user":user_obj,
            "domain":dict(domain_choices),
            "user_role":dict(user_role),
            "position_choices":dict(positon_choices)
        }
        
        if request.method == "POST":
            first_name = request.POST.get("fname")
            last_name = request.POST.get("lname")
            email = request.POST.get("Email")
            Address = request.POST.get("address")
        
            date = request.POST.get("datetime")
            domain_id = request.POST["domain_id"]
            mode = request.POST["mode"]
            
        
            position_id = request.POST.get("position")
            phone = request.POST.get("phone")
            cv = request.FILES["file"]
            print(cv)
            interviewer_id = request.POST.get('interview_id')
            # print(User.objects.filter(id=interviewer_id).values('email'))
            

            Subject = f'Invitation for an interview with visiontrek for position of {domain_id}'

            html_content = render_to_string('email.html',{'first_name':first_name,"last_name":last_name,'datetime':date,'domain':domain_id,'position':position_id})

            msg = EmailMultiAlternatives(Subject,'text_content', 'sajal89304@gmail.com', [email])

            msg.attach_alternative(html_content, "text/html")
            # msg.attach(user_cv.name,user_cv.read(),user_cv.content_type)
            msg.send()
            
            if Interview_meeting.objects.filter(Q(email=email) | Q(phone=phone)).exists():
                attempt = "2nd attempt"
            else:
                attempt = "1st attempt"

            meeting = Interview_meeting.objects.create(first_name=first_name,last_name=last_name,mode_choice=mode,email=email,address=Address,datetime=date,domain_interview=domain_id,position=position_id,phone=phone,user_cv=cv,user=interviewer_id,attempt=attempt)
            
            messages.success(request,"Form Submit Successfully")
            return redirect("create_meeting")
        return render(request,'interview.html',context)
    except:
        messages.error(request,'error occur')
        return render(request,'interview.html')



def Hr_Dashboard(request):
    try:
        interview_meeting_obj = Interview_meeting.objects.filter(attempt="1st attempt")
        int_obj = Interview_meeting.objects.filter(attempt="2nd attempt")
        return render(request,'hr_dashboard.html',{'data':interview_meeting_obj,'data2':int_obj})
    except:
        messages.error(request,'error occur')
        return render(request,'hr_dashboard.html')

def delete_data(request):
    try:
        id = request.GET.get("id")
        user = Interview_meeting.objects.get(id=id)
        user.delete()
        return redirect('hr_dashboard')
    except:
        messages.error(request,'error occur')
        return redirect('hr_dashboard')

def edit_data(request):
    try:
        id = request.GET.get("id")
        inter_obj = Interview_meeting.objects.get(id=id)
        domain_obj = User.objects.all()

        context ={
            "users":inter_obj,
            "user_obj":domain_obj,
            "domain_obj":dict(domain_choices),
            "user_role":dict(user_role),
            "position_choices":dict(positon_choices)
        }
        if request.method == "POST":  
                
            first_name = request.POST.get("fname")
            last_name = request.POST.get("lname")
            email = request.POST.get("Email")
            datetime = request.POST.get("datetime")
            domain = request.POST.get("domain_id")
            position = request.POST.get("position")
            interviewer = request.POST.get("interview_id")
            Address = request.POST.get("address")
            Phone = request.POST.get("phone")
            cv = request.POST.get("uploadfile")
            
            inter_obj.first_name = first_name
            
            inter_obj.last_name = last_name
            inter_obj.email = email
            inter_obj.datetime = datetime
            inter_obj.phone = Phone
            inter_obj.domain_interview = domain
            inter_obj.position = position
            inter_obj.user = interviewer
            inter_obj.address = Address
            inter_obj.user_cv = cv
            inter_obj.save()
            return redirect('hr_dashboard')
        return render(request,'edit_data.html',context)
    except:
        messages.error(request,'error occur')
        return render(request,'edit_data.html')

def hr_send_notification_emp(request):
    user = User.objects.all()
    return render("employee/emp_notification.html",{"user":user})

@csrf_exempt
def send_emp_notification(request):
    message=request.POST.get("message")
    emp=User.objects.get(id=request.user.id)
    token=emp.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Student Management System",
            "body":message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/student_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationEmp(emp_id=User,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")

#  add project by employee
def add_project(request):
    try:
        if request.method == "POST":
            title = request.POST.get("title")
            start_date = request.POST.get('start_date')
            detail = request.POST.get("task_details")
            
            project_obj = Project.objects.create(title=title,start_date=start_date,detail=detail,user_id=request.user)    
        return render(request,'employee/add_project.html')
    except:
        messages.error(request,'error occur')
        return render(request,'employee/add_project.html')


def show_project(request):
    try:
        project_obj = Project.objects.filter(user_id=request.user.id)
        if request.method=="POST":
            pjct_id = request.GET.get('id')
            pjct_obj = Project.objects.get(id=pjct_id)
            status = request.POST.get('status_id')
            if status == "Completed":
                pjct_obj.status = 1
                pjct_obj.end_date = date.today()
                pjct_obj.save()
        context = {
            "project":project_obj
        }
        return render(request,'employee/all_project.html',context)
    except:
        messages.error(request,'error occur')
        return render(request,'employee/all_project.html')


def active_project(request):
    try:
        project_obj = Project.objects.filter(user_id=request.user.id,status=0)
        context = {
            'project':project_obj
        }
        return render(request,'employee/active_project.html',context)
    except:
        messages.error(request,'error occur')
        return render(request,'employee/active_project.html')


def complete_project(request):
    try:
        project_obj = Project.objects.filter(user_id=request.user.id,status=1)
        context = {
            'project':project_obj
        }
        return render(request,'employee/complete_project.html',context)
    except:
        messages.error(request,'error occur')
        return render(request,'employee/complete_project.html')


def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyAa2J8MJTT0ykq6iV_oHWPSPe_9SazCNGE",' \
         '        authDomain: "notification-1a1a5.firebaseapp.com",' \
         '        projectId: "notification-1a1a5",' \
         '        storageBucket: "notification-1a1a5.appspot.com",' \
         '        messagingSenderId: "82591525914",' \
         '        appId: "1:82591525914:web:67e40a1eaaa0d84f6475a3",' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")


