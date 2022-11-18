from django.shortcuts import render
from college import models
from django.http import HttpResponseRedirect
# Create your views here.

# main home page
def home_page_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/index.html')

# for redirecting to admin login/signup button
def admin_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/adminclick.html')

# for redirecting to teacher login/signup button
def teacher_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/teacherclick.html')

# for redirecting to student login/signup button
def student_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/studentclick.html')



