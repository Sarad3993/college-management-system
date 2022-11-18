from django.shortcuts import render
from college import models,forms
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
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


# admin signup 

def admin_signup(request):
    form=forms.AdminSignupForm()
    if request.method=='POST':
        form=forms.AdminSignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()

            admin_group = Group.objects.get_or_create(name='ADMIN')
            admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'college/adminsignup.html',{'form':form})



# teacher signup 
def teacher_signup(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherFormAdditional()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherFormAdditional(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            teacher_group = Group.objects.get_or_create(name='TEACHER')
            teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('teacherlogin')
    return render(request,'college/teachersignup.html',context=mydict)


# student signup

def student_signup(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentFormAdditional()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentFormAdditional(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            student_group = Group.objects.get_or_create(name='STUDENT')
            student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'college/studentsignup.html',context=mydict)
