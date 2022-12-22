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
import requests
from . models import *
def doLogin(request):
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

def emp_profile(request):

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

def reporting(request):

    return render(request,'employee/manage_reporting.html')



@csrf_exempt
def punchin(request):
    print("helllooooo")
    
    date_time_obj = request.POST.get("time")

    status = request.POST.get('punchin') 

    
    print('current',status)
    print(date_time_obj)
    time_obj = date_time_obj[16:24:1]
    date_obj = date_time_obj[0:15]
  
    # a = datetime.strptime(date_obj,'%a %b %m %Y')
    print('aaa',time_obj)

    print('a',date_obj)
  
    datetime_object = datetime.strptime(time_obj, '%H:%M:%S')
    # datetime_object = datetime.strptime(date_time_obj, '%a %b %m %Y %I:%p:%S %X %Z%z%f')
    print('dateeeee',datetime_object)
    
   

    punch = Punch.objects.create(punch_in=datetime_object,punch_date=date_obj, user = request.user)
    if status == "in":
        punch.marked = False 

    punch.save()

    redirect('employee_home')
    



@csrf_exempt
def punchout(request):
    
    
    date_time_obj = request.POST.get("time")
    
    status = request.POST.get('punchout') 

    time_obj = date_time_obj[16:24:1]
    date_obj = date_time_obj[0:15]
    # a = datetime.strptime(date_obj,'%a %b %m %Y')
    print('aaa',time_obj)

    print('a',date_obj)
  
    datetime_object = datetime.strptime(time_obj, '%H:%M:%S')
    # datetime_object = datetime.strptime(date_time_obj, '%a %b %m %Y %I:%p:%S %X %Z%z%f')
    print('dateeeee',datetime_object)
    print('oye',datetime_object-datetime_object)
    
   

    punch = Punch.objects.filter(user=request.user).last()
    print('last',punch)
    punch.punch_out = datetime_object
    if status == "out":
        punch.marked = True 
        punch.save()
        print(punch.marked)
    

    redirect('employee_home')
    
    




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
    user_obj=User.objects.get(id=10)
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