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
                return redirect('dashboard')
                
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
    
    date_time_obj = request.POST["time"]
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
    
    
    punch = Punch.objects.create(punch_in=datetime_object,punch_date=date_obj,marked=status)
    
    date_list = list(date_time_obj)
    return JsonResponse(json.dumps(date_time_obj),content_type="application/json",safe=False)




    '2022-12-12 04:39:05.182486'