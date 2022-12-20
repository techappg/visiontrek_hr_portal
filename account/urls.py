from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views
from hr.views import *
urlpatterns = [
    path('',doLogin,name='login'),
    path('employee_home',employee_home,name='employee_home'),
    path('punchin/',punchin,name='punchin'),
    path('punchout/',punchout,name='punchout'),
    path('notifi',index,name='notifi'),
    path('emp_profile',emp_profile,name='emp_profile'),
    path('user_fcmtoken/',user_fcmtoken,name='user_fcmtoken'),
    path('firebase-messaging-sw.js',showFirebaseJS,name="show_firebase_js"),



#  password reset urls


    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),

    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),



]
