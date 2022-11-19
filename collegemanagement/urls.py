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
    path('admin-add-teacher', views.admin_add_teacher,name='admin-add-teacher'),
    path('admin-view-teacher', views.admin_view_teacher,name='admin-view-teacher'),
    path('admin-approve-teacher', views.admin_approve_teacher,name='admin-approve-teacher'),
    path('approve-teacher/<int:pk>', views.approve_teacher,name='approve-teacher'),
    path('disapprove-teacher/<int:pk>', views.disapprove_teacher,name='disapprove-teacher'),
    path('update-teacher/<int:pk>', views.update_teacher,name='update-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher,name='delete-teacher'),
    path('admin-student', views.admin_student_section,name='admin-student'),
    path('admin-add-student', views.admin_add_student,name='admin-add-student'),
    path('admin-view-student', views.admin_view_student,name='admin-view-student'),
    path('admin-approve-student', views.admin_approve_student,name='admin-approve-student'),
    path('approve-student/<int:pk>', views.approve_student,name='approve-student'),
    path('disapprove-student/<int:pk>', views.disapprove_student,name='disapprove-student'),
    path('update-student/<int:pk>', views.update_student,name='update-student'),
    path('delete-student/<int:pk>', views.delete_student,name='delete-student'),
    path('admin-notice', views.admin_notice,name='admin-notice'),
    path('delete-notice/<int:pk>', views.admin_delete_notice,name='delete-notice'),
    path('teacher-dashboard', views.teacher_dashboard,name='teacher-dashboard'),
    path('teacher-notice', views.teacher_notice,name='teacher-notice'),
    path('teacher-attendance', views.teacher_attendance,name='teacher-attendance'),
    path('teacher-take-attendance/<str:faculty>', views.take_attendance,name='teacher-take-attendance'),
    path('teacher-view-attendance/<str:faculty>', views.view_attendance,name='teacher-view-attendance'),
    path('student-dashboard', views.student_dashboard,name='student-dashboard'),
    
    
]