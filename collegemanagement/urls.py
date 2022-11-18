"""collegemanagement URL Configuration
"""
from django.contrib import admin
from django.urls import path
from college import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.home_page_view,name=''),
    path('adminclick',views.admin_click_view),
    path('teacherclick',views.teacher_click_view),
    path('studentclick',views.student_click_view),
    path('adminsignup',views.admin_signup),
     path('studentsignup', views.student_signup),
    path('teachersignup', views.teacher_signup),
    
    
    
]
