from django.shortcuts import render,redirect
from college import models,forms
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
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


#for checking user is teacher, student or admin

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        accountapproval=models.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher-dashboard')
        else:
            return render(request,'college/teacher_approval_pending.html')
    elif is_student(request.user):
        accountapproval=models.Student.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request,'college/student_approval_pending.html')
        
        
#Admin dashboard

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard(request):
    teachercount=models.Teacher.objects.all().filter(status=True).count()
    pendingteachercount=models.Teacher.objects.all().filter(status=False).count()

    studentcount=models.Student.objects.all().filter(status=True).count()
    pendingstudentcount=models.Student.objects.all().filter(status=False).count()

    teachersalary=models.Teacher.objects.filter(status=True).aggregate(Sum('salary',default=0))
    pendingteachersalary=models.Teacher.objects.filter(status=False).aggregate(Sum('salary'))

    studentfee=models.Student.objects.filter(status=True).aggregate(Sum('fee',default=0))
    pendingstudentfee=models.Student.objects.filter(status=False).aggregate(Sum('fee'))

    notice=models.Notice.objects.all()

    #aggregate function return dictionary so fetch data from dictionay
    mydict={
        'teachercount':teachercount,
        'pendingteachercount':pendingteachercount,

        'studentcount':studentcount,
        'pendingstudentcount':pendingstudentcount,

        'teachersalary':teachersalary['salary__sum'],
        'pendingteachersalary':pendingteachersalary['salary__sum'],

        'studentfee':studentfee['fee__sum'],
        'pendingstudentfee':pendingstudentfee['fee__sum'],

        'notice':notice

    }

    return render(request,'college/admin_dashboard.html',context=mydict)