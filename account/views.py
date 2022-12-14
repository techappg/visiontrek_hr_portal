from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from account.EmailBackEnd import EmailBackEnd
from django.views.decorators.csrf import csrf_exempt
from hr.models import Punch
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



@csrf_exempt
def punchin(request):
    print("helllooooo")
    
    date_time_obj = request.POST.get("time")
    print("aaaaa",date_time_obj)
    status = request.POST.get('punchin') 

    
    print(status)
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
        punch.marked == True 

    punch.save()

    
    date_list = list(date_time_obj)
    return JsonResponse(json.dumps(date_time_obj),content_type="application/json",safe=False)


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
    
   

    punch = Punch.objects.filter(user=request.user).last()
    print('last',punch)
    punch.punch_out = datetime_object
    if status == "out":
        punch.marked == False 

    punch.save()

    
    date_list = list(date_time_obj)
    return JsonResponse(json.dumps(date_time_obj),content_type="application/json",safe=False)



# def send_notification(registration_ids , message_title , message_desc):
#     print("enterrree")
#     fcm_api = "AAAADoYteDs:APA91bFa8xsUXzNvtt4AjcDDX6zCUfZKd67sNkOwLIJpENBtFJpES-AnWpzBStc5-QHd9m6r4RuGudXrbChtoDsizfUBdEMUP7yqFruLYefElCipcUeSJCailaCNFya0YwALP_vrqRWl"
#     url = "https://fcm.googleapis.com/fcm/send"

        
#     headers = {
#     'Content-Type':'application/json',
#     'Authorization': 'key='+fcm_api,
#     }

#     payload = {
#         'registration_ids' :registration_ids,
#         'priority' : 'high',
#         'notification' : {
#             'body' : message_desc,
#             'title' : message_title,
          
#         }
#     }
#     print("payload",payload)

#     result = requests.post(url,data=json.dumps(payload), headers=headers)
#     print(result.json())


# def index(request):
#     print("shhfhd")
#     # if request.method=="POST":
#     # a = User.objects.create(first_name="fdkfdf")
#     message_desc="hello"
#     message_title="createddd"
#     registration_ids=["d0NxWGqlPF2R7DzIs6YVds:APA91bEVTEDTpG2-ymc2-sIeumhhuszyZMus87JK8SFgr1ufcTTARCwbyNeDUkEicFstOjreCJuw9n8bSJ_yktp-IRJQ8n7QDTGsuoovXyRNqlRuB_8eLHKTi2XQDblgEtMU9MVC8neV"]
#     send_notification(registration_ids , message_title , message_desc)
#     print("fkfkfk")
#     return HttpResponse("NOTIFIUCSTN SEBDDD")
# return render(request,'index.html')



# def send_notification(registration_ids, message_title, message_desc):
#     print("enterrree")
#     fcm_api = "AAAAmPVuHa0:APA91bFG81PmXDKWu_HSNXqYbsPmJtrE4GxhQdIA3BEWxWgucmQr9H7egbnQwGstHBZh0G99DKcO8mnmhR8lSDxTUxznQYTkSEQSBaaPfN8V9nnLkfhdniKJffpXD4PettPcin2tuocq"
#     url = "https://fcm.googleapis.com/fcm/send"

#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'key=' + fcm_api,
#     }

#     payload = {
#         'registration_ids': registration_ids,
#         'priority': 'high',
#         'notification': {
#             'body': message_desc,
#             'title': message_title,

#         }
#     }
#     print("payload", payload)

#     result = requests.post(url, data=json.dumps(payload), headers=headers)
#     print(result.json())


# def index(request):
#     print("shhfhd")
#     # if request.method=="POST":
#     # a = User.objects.create(first_name="fdkfdf")
#     message_desc = "hello"
#     message_title = "createddd"
#     registration_ids = [
#         "d0NxWGqlPF2R7DzIs6YVds:APA91bEVTEDTpG2-ymc2-sIeumhhuszyZMus87JK8SFgr1ufcTTARCwbyNeDUkEicFstOjreCJuw9n8bSJ_yktp-IRJQ8n7QDTGsuoovXyRNqlRuB_8eLHKTi2XQDblgEtMU9MVC8neV"]
#     send_notification(registration_ids, message_title, message_desc)
#     print("fkfkfk")
#     return HttpResponse("NOTIFIUCSTN SEBDDD")
def send_notification(registration_ids, message_title, message_desc):
    print("enterrree")
    fcm_api = "AAAAmPVuHa0:APA91bFG81PmXDKWu_HSNXqYbsPmJtrE4GxhQdIA3BEWxWgucmQr9H7egbnQwGstHBZh0G99DKcO8mnmhR8lSDxTUxznQYTkSEQSBaaPfN8V9nnLkfhdniKJffpXD4PettPcin2tuocq"
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