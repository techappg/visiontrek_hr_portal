from django import forms
from account.models import *

class AddUserForm(forms.Form):
    email = forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    try:
        user = User.objects.all()
        user_list = []
        for i in user:
            i_user = (i.id, i.usertype)
            user_list.append(i_user)
    except:
        user_list = []

    try:
        pos_list = []
        position = Pos_choice.objects.all()
        for i in position:
            i_pos = (i.id,i.position)
            pos_list.append(i_pos)
    except:
        pos_list = []

    try:
        dom_list = []
        domain = Domain_name.objects.all()
        for i in domain:
            dom = (i.id,i.name)
            dom_list.append(dom)
    except:
        dom_list = []


    usertype = forms.ChoiceField(label="usertype", choices=user_list, widget=forms.Select(attrs={"class":"form-control"}))
    position = forms.ChoiceField(label="position", choices=pos_list, widget=forms.Select(attrs={"class":"form-control"}))
    domain = forms.ChoiceField(label="domain", choices=user_list, widget=forms.Select(attrs={"class":"form-control"}))
    