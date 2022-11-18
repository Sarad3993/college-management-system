"""collegemanagement URL Configuration
"""
from django.contrib import admin
from django.urls import path
from college import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.home_page_view,name=''),
    path('adminclick',views.admin_click_view),
    path('teacherclick',views.teacher_click_view),
    path('studentclick',views.student_click_view),
    path('adminsignup',views.admin_signup),
    path('studentsignup', views.student_signup),
    path('teachersignup', views.teacher_signup),
    path('adminlogin', LoginView.as_view(template_name='college/adminlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='college/studentlogin.html')),
    path('teacherlogin', LoginView.as_view(template_name='college/teacherlogin.html')),
    path('afterlogin', views.afterlogin,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='college/index.html'),name='logout'),
    path('admin-dashboard', views.admin_dashboard,name='admin-dashboard'),
    path('admin-teacher', views.admin_teacher_section,name='admin-teacher'),
    
]
