from django.shortcuts import render, redirect
from . models import *
from account.models import *
from django.db.models import Q
from django.contrib import messages
# Create your views here.


# def status(request,id):
#     if request.method=='POST':
#         status=request.POST['status']
#         Interview_meeting.objects.filter(id=id).update(status=status)
   
#     return redirect('showhrdashboard')

def dashboard(request):
    return render(request,'base.html')

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
        "pos":pos_obj
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
        cv = request.FILES.get("uploadfile")
        interviewer_id = request.POST.get('interview_id')
        # print(User.objects.filter(id=interviewer_id).values('email'))
        interviewer = User.objects.get(id=interviewer_id)
        # validationd=
        # error_message = None

        # if(not name):
        #     error_message = "Name is required !!"
        # elif not email:
        #     error_message = "Email is required"
    

        
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
    print(user_obj.first_name)
    print(user_obj.last_name)

    context ={
        "user":user_obj
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

