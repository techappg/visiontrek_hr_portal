from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from account.EmailBackEnd import EmailBackEnd
from django.views.decorators.csrf import csrf_exempt
from hr.models import Punch
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
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

    date = request.POST.get('time')
    print(date)
    punch = Punch.objects.create(punch_in=date)
    date_list = list(date)
    return JsonResponse(json.dumps(date_list),content_type="application/json",safe=False)