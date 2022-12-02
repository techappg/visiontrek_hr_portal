from django.shortcuts import render, redirect
from . models import *
from account.models import *
from django.db.models import Q
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives,send_mail,EmailMessage
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
    print(office_obj.user)
    user_obj = User.objects.all()
    context = {
        'office':office_obj,
        'user':user_obj
    }
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


