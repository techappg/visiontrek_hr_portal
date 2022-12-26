from django.shortcuts import render, redirect
from . models import *
from account.models import *
from django.db.models import Q
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives,send_mail,EmailMessage
from .forms import AddUserForm
from datetime import datetime, date
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import HttpResponse
from . models import task_choice
import json
# Create your views here.


# def status(request,id):
#     if request.method=='POST':
#         status=request.POST['status']
#         Interview_meeting.objects.filter(id=id).update(status=status)
   
#     return redirect('showhrdashboard')
def hr_leave_view(request):
    leaves = LeaveReportEmployee.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request,'emp_leave_view.html',context)

def Empl_leave_apply(request):
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

def python_team(request,status):
    user = Domain_name.objects.get(name=status)
    user_obj = User.objects.filter(domain_id=user.id)
    
    return render(request,'employee/python_team.html',{'user':user_obj})

def emp_leave_view(request):
    user_obj = User.objects.get(username=request.user)

    leave_obj = LeaveReportEmployee.objects.filter(emp_id=user_obj)
    
    return render(request,'employee/emp_leave_view.html',{'leaves':leave_obj})

def emp_leave_approve(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('hr_leave_view')


def emp_leave_reject(request, leave_id):
    leave = LeaveReportEmployee.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('hr_leave_view')

def emp_task_view(request):
    task_obj = Task.objects.filter(user_id=request.user.id)
    
    date_obj = date.today()

    context = {
        "task":task_obj,
        'date':date_obj
    }
    return render(request,'employee/show_task.html',context)

def dashboard(request):
    return render(request,'employee/base.html')

def employee_home(request):
    punch = Punch.objects.filter(user=request.user)
    
    punch_obj = Punch.objects.filter(user=request.user).last()
    a = punch_obj.marked
    b = punch_obj.punch_out
    c = punch_obj.punch_in
    if b!= None:
        d =datetime.combine(date.today(), b) - datetime.combine(date.today(), c)

        print(d)
    else:
        d = None
    context = { 
        'punch':punch,
        'mark':a,
        'out':d
    }
    
    return render(request,'employee/emp_dashboard.html',context)

def add_task(request):
    if request.method=="POST":
  
        task = request.POST.get("task_val")
        file = request.FILES.get('imagesfiles')
        detail = request.POST.get("taskdetail")
        a = date.today()
        print('oyeeeeeeeeeeeeee',a)
        task_obj = Task.objects.create(task_type=task,screenshot=file,detail=detail,user_id=request.user,create_task_date=date.today())
    
    return render(request,'employee/add_task.html',{"choice":dict(task_choice)})

def AddUser(request):
    form = AddUserForm(request.POST)

    if request.method == "POST":
     
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            user_id = form.cleaned_data['usertype']
            pos_id = form.cleaned_data['position']
            dom_id = form.cleaned_data['domain']

        
            try:
                user = User.objects.create(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3,address=address)
                

                user_obj = User.objects.get(id=user_id)
                user.usertype = user_obj

                pos_obj = Pos_choice.objects.get(id=pos_id)
                user.position = pos_obj

                dom_obj = Domain_name.objects.get(id=dom_id)
                user.domain = dom_obj
                user.save()
                messages.success(request, "User Added Successfully!")
                return redirect('dashboard')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('dashboard')
        else:
            return redirect('add_student')
    print(form)
    return render(request,'adduser.html',{"form":form})




def home(request):
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

def office_meeting(request):
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


def office_meeting_data(request):
    office_obj = Office_meeting.objects.all()
    user_obj = User.objects.all()
    
    context = {
        'office':office_obj,
        'user':user_obj
    }
    return render(request,'office_data.html',context)

def delete_data_offc(request):
        id = request.GET.get("id")
        user = Office_meeting.objects.get(id=id)
        user.delete()
        messages.success(request,"Delete Data Successfully")

        return redirect('office_meeting_data')

def edit_office_meeting(request):
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

def selected_data(request):
    
    select = Interview_meeting.objects.filter(status='Selected')
    return render(request,'select.html',{'select':select})
    
def reject_data(request):
    
    reject = Interview_meeting.objects.filter(status='Rejected')
    return render(request,'reject.html',{'reject':reject})

def hold_data(request):
    
    hold = Interview_meeting.objects.filter(status='Hold')
    return render(request,'hold.html',{'hold':hold})




def create_meeting(request):
    domain_obj = Domain_name.objects.all()
    user_obj = User.objects.all()
    pos_obj = Pos_choice.objects.all()
    context = {
        "domain":domain_obj,
        "user":user_obj,
        "pos":pos_obj,
    }
    
    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("Email")
        Address = request.POST.get("address")
    
        date = request.POST.get("datetime")
        domain_id = request.POST["domain_id"]
        mode = request.POST["mode"]
        
        domain = Domain_name.objects.get(id=domain_id)
    
        position_id = request.POST.get("position")
        position = Pos_choice.objects.get(id=position_id)
        phone = request.POST.get("phone")
        cv = request.FILES["file"]
        print(cv)
        interviewer_id = request.POST.get('interview_id')
        # print(User.objects.filter(id=interviewer_id).values('email'))
        interviewer = User.objects.get(id=interviewer_id)

        Subject = f'Invitation for an interview with visiontrek for position of {domain}'

        html_content = render_to_string('email.html',{'first_name':first_name,"last_name":last_name,'datetime':date,'domain':domain,'position':position})

        msg = EmailMultiAlternatives(Subject,'text_content', 'sajal89304@gmail.com', [email])

        msg.attach_alternative(html_content, "text/html")
        # msg.attach(user_cv.name,user_cv.read(),user_cv.content_type)
        msg.send()
        
        if Interview_meeting.objects.filter(Q(email=email) | Q(phone=phone)).exists():
            attempt = "2nd attempt"
        else:
            attempt = "1st attempt"

        meeting = Interview_meeting.objects.create(first_name=first_name,last_name=last_name,mode_choice=mode,email=email,address=Address,datetime=date,domain_interview=domain,position=position,phone=phone,user_cv=cv,user=interviewer,attempt=attempt)
        
        messages.success(request,"Form Submit Successfully")


        
        return redirect("create_meeting")

    return render(request,'interview.html',context)



def Hr_Dashboard(request):
    interview_meeting_obj = Interview_meeting.objects.filter(attempt="1st attempt")
    int_obj = Interview_meeting.objects.filter(attempt="2nd attempt")
  
    return render(request,'hr_dashboard.html',{'data':interview_meeting_obj,'data2':int_obj})




def delete_data(request):
        id = request.GET.get("id")
        user = Interview_meeting.objects.get(id=id)
        user.delete()
        return redirect('hr_dashboard')


def edit_data(request):
    id = request.GET.get("id")
    user_obj = Interview_meeting.objects.get(id=id)
    domain_obj = Domain_name.objects.all()
    pos_obj = Pos_choice.objects.all()
    user = User.objects.all()


    context ={
        "users":user_obj,
        "domain":domain_obj,
        "pos":pos_obj,
        "new_user":user

    }

    print("context::", context)

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
        
        user_obj.first_name = first_name
        
        user_obj.last_name = last_name
        user_obj.email = email
        user_obj.datetime = datetime
        user_obj.phone = Phone
        user_obj.domain_interview = domain
        user_obj.position = position
        user_obj.user = interviewer
        user_obj.address = Address
        user_obj.user_cv = cv
        user_obj.save()
        return redirect('hr_dashboard')

    return render(request,'edit_data.html',context)

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
    if request.method == "POST":
        title = request.POST.get("title")
        start_date = request.POST.get('start_date')
        status = request.POST.get('status')
        detail = request.POST.get("task_details")
        
        project_obj = Project.objects.create(title=title,start_date=start_date,status=status,detail=detail,user_id=request.user)    
    return render(request,'employee/add_project.html')

def show_project(request):
    project_obj = Project.objects.filter(user_id=request.user.id)
    context = {
        "project":project_obj
    }
    return render(request,'employee/all_project.html',context)

def active_project(request):
    project_obj = Project.objects.filter(user_id=request.user.id,status=1)
    context = {
        'project':project_obj
    }
    return render(request,'employee/active_project.html',context)

def complete_project(request):
    project_obj = Project.objects.filter(user_id=request.user.id,status=0)
    context = {
        'project':project_obj
    }
    return render(request,'employee/complete_project.html',context)

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


