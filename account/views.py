from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from account.EmailBackEnd import EmailBackEnd


def doLogin(request):
    if request.method == "POST":
     
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        print(user)
        if user:
            login(request, user)
            user_type = user.usertype
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


def employee_home(request):
    return render(request,'employee/home.html')