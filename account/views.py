from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from account.EmailBackEnd import EmailBackEnd
from django.views.decorators.csrf import csrf_exempt
from hr.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from datetime import datetime
from django.utils.timezone import timedelta
from django.views.generic.edit import UpdateView  
from django.views import View
import requests
from django.contrib.auth.hashers import make_password

from . models import *
from django.shortcuts import get_object_or_404

def doLogin(request):
    try:
        if request.method == "POST":
        
            user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
            print(user)
            if user:
                login(request, user)
                user_type = user.user_type
                print(user_type)
                # return redirect('dashboard')
                #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
                if user_type == '1':
                    return redirect('hr_dashboard')
                    
                else :
                    # return HttpResponse("Staff Login")
                    return redirect('employee_home')
                    
            
                # else:
                #     messages.error(request, "Invalid Login!")
                #     return redirect('login')
            else:
                messages.error(request, "Invalid Login Credentials!")
                #return HttpResponseRedirect("/")
                return redirect('login')
        return render(request,'login.html')
    except:
        return render(request,'login.html')


def hr_profile(request):
    try:
        user_id = request.user.id
        user_obj = User.objects.get(id=user_id)
        context = {
            'user':user_obj
        }
        if request.method == "POST":
            profile_pic = request.FILES['profile_pic']
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            address = request.POST.get("address")
            password = request.POST.get("password")
            print('passsword',password)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.address = address
            user_obj.profile_pic = profile_pic
            if password:
                user_obj.password = make_password(password)
            user_obj.save()
            messages.success(request,"profile update successfully")
        return render(request,'hr_profile.html')
    except:
        messages.error(request, "profile not updated")
        return render(request,'hr_profile.html')


def emp_profile(request):
    try:
        user_id = request.user.id
        user_obj = User.objects.get(id=user_id)
        context = {
            'user':user_obj
        }
        if request.method == "POST":
            profile_pic = request.FILES['profile_pic']
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            address = request.POST.get("address")
            password = request.POST.get("password")
            print('passsword',password)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.address = address
            user_obj.profile_pic = profile_pic
            if password:
                user_obj.password = make_password(password)
            user_obj.save()
            messages.success(request,"profile update successfully")
        return render(request,'employee/emp_profile.html')
    except:
        messages.error(request, "profile not updated")
        return render(request,'employee/emp_profile.html')


@csrf_exempt
def user_fcmtoken(request):
    try:
        token = request.POST.get("token")
        user = User.objects.get(user_type=request.user.user_type)
        user.fcm_token = token
        user.save()
        return HttpResponse("True")
    except: return HttpResponse("False")

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "YOUR_API_KEY",' \
         '        authDomain: "FIREBASE_AUTH_URL",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '        projectId: "FIREBASE_PROJECT_ID",' \
         '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
         '        messagingSenderId: "FIREBASE_SENDER_ID",' \
         '        appId: "FIREBASE_APP_ID",' \
         '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
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


def emp_task_data(request):
    try:
        emp_id = request.GET.get("id")
        
        emp_obj = Task.objects.get(id=emp_id)
        
        return render(request,'employee/emp_task_data.html',{'emp':emp_obj})
    except:
        messages.error(request, "Error occur")
        return render(request,'employee/emp_task_data.html')




@csrf_exempt
def punchin(request):
    if request.method == 'POST':
        
        date_time_obj = request.POST.get("time")
   
        status = request.POST.get('punchin') 
        
    
        time_obj = date_time_obj[16:24:1]
        date_obj = date_time_obj[0:15]
        # a = datetime.strptime(date_obj,'%a %b %m %Y')
    
        datetime_object = datetime.strptime(time_obj, '%H:%M:%S')
        print('hellloooooo',type(datetime_object))
        # datetime_object = datetime.strptime(date_time_obj, '%a %b %m %Y %I:%p:%S %X %Z%z%f')
    
        punch = Punch.objects.create(punch_in=datetime_object,punch_date=date_obj, user = request.user)
        if status == "in":
            punch.marked = True 
            punch.save()
    
        # redirect('employee_home')
    
        return JsonResponse({'status':'Save'})
    else:
        return JsonResponse({'status':0})

    
@csrf_exempt
def punchout(request):
    date_time_obj = request.POST.get("time")
    status = request.POST.get('punchout') 
    time_obj = date_time_obj[16:24:1]
    date_obj = date_time_obj[0:15]
    # a = datetime.strptime(date_obj,'%a %b %m %Y')
   
    datetime_object = datetime.strptime(time_obj, '%H:%M:%S')
    print('nkvnoernvini',type(datetime_object))



    punch = Punch.objects.filter(user=request.user).last()

    punch.punch_out = datetime_object
    a = punch.punch_out
    b = punch.punch_in
    print(f'helllllooooo{a}anddd{b}')

    punch.save()
    if status == "out":
        punch.marked = False 
        punch.save()

        return JsonResponse({'status':'Save'})
    else:
        return JsonResponse({'status':0})   
    

def send_notification(registration_ids, message_title, message_desc):
    print("enterrree")
    fcm_api = "AAAAEzrWrBo:APA91bFb1gozb9_NNJ6XYQxfCrUsmZQIjGZDYRbInRELckVwcuK3DwFB6cP-SuWzC7a4-gYe_r1Sg9eNj6pDEsMSyZZ_C5Q4U4LDrlfST-ojxKmg1YBnBtahhRSRE8wT8rNWltfgnPag"
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + fcm_api,
    }

    payload = {
        'registration_ids': registration_ids,
        'priority': 'high',
        'notification': {
            'body': message_desc,
            'title': message_title,

        }
    }
    print("payload", payload)

    result = requests.post(url, data=json.dumps(payload), headers=headers)
    print(result.json())


def index(request):
    print("shhfhd")
    # if request.method=="POST":
    # a = User.objects.create(first_name="fdkfdf")
    message_desc = "hello"
    message_title = "createddd"
    registration_ids = [
        "eg5UvozF-_ayNTg1F_qA9L:APA91bEitpZZRlm0jwIsBjav1WaLzV-VFTaLfdMwLHW8KfMfVZOvWLdLJ4v7C4Evu1776ehgqtZhh5FFJV95J2X1UdjHy895mHka6saJcn_khjiinWtDI75U7mqQRincO5noX6YyWfq4"]
    send_notification(registration_ids, message_title, message_desc)
    print("fkfkfk")
    return HttpResponse("NOTIFIUCSTN SEBDDD")

@csrf_exempt
def emp_fcm_save(request):
    token=request.POST.get("token")
    print('token')
    try:
        emp=User.objects.get(id=request.user.id)
        emp.fcm_token=token
        emp.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")
@csrf_exempt
def hr_fcm_save(request):
    token=request.POST.get("token")
    print('token')
    try:
        emp=User.objects.get(id=request.user.id)
        emp.fcm_token=token
        emp.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def send(request):
    tkn = User.objects.get(id=request.user.id)

    resgistration  = [tkn.fcm_token]
    print(resgistration)
    send_notification(resgistration , 'Manik push notification test','notification trial')
    return HttpResponse("sent")

@csrf_exempt
def send_hr_notification(request):
    
    a_date=request.POST.get("aply_date")
    message=request.POST.get("message")
    print(a_date)
    print(message)
    user_obj=User.objects.get(id=1)
    a = user_obj.id
    token=user_obj.fcm_token
    print(token)
    fcm_api = "AAAAEzrWrBo:APA91bFb1gozb9_NNJ6XYQxfCrUsmZQIjGZDYRbInRELckVwcuK3DwFB6cP-SuWzC7a4-gYe_r1Sg9eNj6pDEsMSyZZ_C5Q4U4LDrlfST-ojxKmg1YBnBtahhRSRE8wT8rNWltfgnPag"

    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Leave apply by employee",
            "body":message,
            "click_action": "http://127.0.0.1:8000/emp_leave_view/",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key="+fcm_api}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    print(f"hereeee")
    notification=NotificationEmp(emp_id_id=a,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")
# emp_name text

@csrf_exempt
def new(request):
    if request.method == "POST":
        print("inside bro")
        id_emp = request.POST.get("id_emp")
        print("empiddddd",id_emp)
        emp_name=request.POST.get("emp_name")
        text=request.POST.get("text")
        user_obj=User.objects.get(id=id_emp)
        token=user_obj.fcm_token
        print(token)
        fcm_api = "AAAAEzrWrBo:APA91bFb1gozb9_NNJ6XYQxfCrUsmZQIjGZDYRbInRELckVwcuK3DwFB6cP-SuWzC7a4-gYe_r1Sg9eNj6pDEsMSyZZ_C5Q4U4LDrlfST-ojxKmg1YBnBtahhRSRE8wT8rNWltfgnPag"

        url="https://fcm.googleapis.com/fcm/send"
        body={
            "notification":{
                "title":"Leave apply by employee",
                "body":text,
                "click_action": "http://127.0.0.1:8000/send_emp_notification/",
            },
            "to":token
        }
        headers={"Content-Type":"application/json","Authorization":"key="+fcm_api}
        data=requests.post(url,data=json.dumps(body),headers=headers)
        
        print(data.text)
        return HttpResponse("True")


@csrf_exempt
def send_emp_notification(request):
    if request.method == "POST":
        print("helllooooooooooooooooooooooooooo")
    id_emp = request.POST.get("id_emp")
    print("empiddddd",id)
    emp_name=request.POST.get("emp_name")

    text=request.POST.get("text")

    user_obj=User.objects.get(id=id_emp)
    token=user_obj.fcm_token
    print(token)
    fcm_api = "AAAAEzrWrBo:APA91bFb1gozb9_NNJ6XYQxfCrUsmZQIjGZDYRbInRELckVwcuK3DwFB6cP-SuWzC7a4-gYe_r1Sg9eNj6pDEsMSyZZ_C5Q4U4LDrlfST-ojxKmg1YBnBtahhRSRE8wT8rNWltfgnPag"

    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Leave apply by employee",
            "body":text,
            "click_action": "http://127.0.0.1:8000/send_emp_notification/",
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key="+fcm_api}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    
    print(data.text)
    return HttpResponse("True")

def logout_view(request):    
    logout(request)
    return redirect('login')

def edit_task(request):
    try:
        edit_id = request.GET.get("id")
        emp_obj = Task.objects.get(id=edit_id)
        
        context = {
            'task':emp_obj,
            "choice":dict(task_choice)
        }
        messages.success(request,"Edit task successfully")
        return render(request,'employee/edit_task.html',context)
    except:
        messages.error(request, "task not update!!")
        return render(request,'employee/edit_task.html')


def delete_task(request):
    try:
        task_id = request.GET.get('id')
        print('taskkkk idddddddd',task_id)
        task_obj = Task.objects.get(id=task_id)
        task_obj.delete()
        messages.success(request,"Delete task successfully")

        return redirect('emp_task_view')
    except:
        messages.error(request, "task not deleted")
        return redirect('emp_task_view')


def reporting(request):
    try:
        users_obj = User.objects.all()
        if request.method == "POST":
            report_to = request.POST.get('report_id')
            user_obj = User.objects.get(id=report_to)
            a = user_obj.id
            print('aaaaaaaaa',a)
            reporting_from = request.POST.get('reporting_from')
            reporting_till = request.POST.get('reporting_till')
            report_obj = Reporting.objects.create(new_reporting_to=user_obj,report_from=reporting_from,report_till=reporting_till,report_by=request.user)
        return render(request,'employee/manage_reporting.html',{'user':users_obj})
    except:
        messages.error(request, "error occur")
        return render(request,'employee/manage_reporting.html')


def report_to(request):
    try:
        user_obj = User.objects.get(id=request.user.id)
        report_to_user = user_obj.reporting_to
        emp = User.objects.get(username=report_to_user)
        return render(request,'employee/report_to.html',{'emp':emp})
    except:
        messages.error(request, "error occur")
        return render(request,'employee/report_to.html')

def report_by(request):
    try:
        report_obj = User.objects.filter(reporting_to=request.user)
    
        return render(request,'employee/report_by.html',{'emp':report_obj})
    except:
        messages.error(request, "error occur")
        return render(request,'employee/report_by.html')


def show_task_rep(request):
    try:
        tsk_name = request.GET.get("name")
        id = User.objects.get(username=tsk_name)
        task_obj = Task.objects.filter(user_id=id)
        return render(request,'employee/show_task_rep.html',{'task':task_obj})
    except:
        messages.error(request, "error occur")
        return render(request,'employee/show_task_rep.html')


def show_pjct_rep(request):
    try:
        pjct_name = request.GET.get("name")
        id = User.objects.get(username=pjct_name)

        pjct_obj = Project.objects.filter(user_id=id)
        return render(request,'employee/show_pjct_rep.html',{'project':pjct_obj})
    except:
        messages.error(request, "error occur")
        return render(request,'employee/show_pjct_rep.html')


def chat_view(request):
    to_id = request.GET.get("name")
    user_obj = User.objects.get(username=to_id)
    print('phone',user_obj.phone)
    phone = user_obj.phone
    if phone is None:
        phone = 9999999999
    to_instance = User.objects.get(username=to_id)
    by_id = request.user
    chat_create=Thread.objects.filter(Q(first_person=to_instance,second_person=by_id)|Q(first_person=by_id,second_person=to_instance))

    if chat_create:

        for i in chat_create:
            threads = Thread.objects.filter(id=i.id)
        
        context = {
            'Threads': threads,
            'to_name': to_id,
            'phone': phone
        }
        return render(request,'chat.html',context)
    else:

        chat_create = Thread.objects.create(first_person=to_instance,second_person=by_id)  
        threads= Thread.objects.filter(id=chat_create.id)
        
    
        context = {
            'Threads': threads,
            'to_name': to_id
        } 

    return render(request,'chat.html',locals())

def start_timer(request):
    deadline = datetime.datetime.now() + datetime.timedelta(minutes=540)
    remaining_time = deadline - datetime.datetime.now()
    timer = CountdownTimer.objects.create(deadline=deadline, remaining_time=remaining_time)
    timer.save()
    return render(request, 'employee/emp_dashboard.html', {'timer': timer})

def update_timer(request):
    timer = CountdownTimer.objects.get(id=1)
    remaining_time = timer.deadline - datetime.datetime.now()
    timer.remaining_time = remaining_time
    timer.save()
    return render(request, 'employee/emp_dashboard.html', {'timer': timer})