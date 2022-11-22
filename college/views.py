from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from college import forms, models
# Create your views here.

# main home page
def home_page_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "college/index.html")


# for redirecting to admin login/signup button
def admin_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "college/adminclick.html")

# for redirecting to teacher login/signup button
def teacher_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "college/teacherclick.html")

# for redirecting to student login/signup button
def student_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "college/studentclick.html")


# admin signup
def admin_signup(request):
    form = forms.AdminSignupForm()
    if request.method == "POST":
        form = forms.AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            admin_group = Group.objects.get_or_create(name="ADMIN")
            admin_group[0].user_set.add(user)

            return HttpResponseRedirect("adminlogin")
    return render(request, "college/adminsignup.html", {"form": form})


# teacher signup
def teacher_signup(request):
    form1 = forms.TeacherUserForm()
    form2 = forms.TeacherFormAdditional()
    mydict = {"form1": form1, "form2": form2}
    if request.method == "POST":
        form1 = forms.TeacherUserForm(request.POST)
        form2 = forms.TeacherFormAdditional(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()

            teacher_group = Group.objects.get_or_create(name="TEACHER")
            teacher_group[0].user_set.add(user)

        return HttpResponseRedirect("teacherlogin")
    return render(request, "college/teachersignup.html", context=mydict)


# student signup
def student_signup(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentFormAdditional()
    mydict = {"form1": form1, "form2": form2}
    if request.method == "POST":
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentFormAdditional(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()

            student_group = Group.objects.get_or_create(name="STUDENT")
            student_group[0].user_set.add(user)

        return HttpResponseRedirect("studentlogin")
    return render(request, "college/studentsignup.html", context=mydict)


# for checking user is teacher, student or admin


def is_admin(user):
    return user.groups.filter(name="ADMIN").exists()


def is_teacher(user):
    return user.groups.filter(name="TEACHER").exists()


def is_student(user):
    return user.groups.filter(name="STUDENT").exists()


def afterlogin(request):
    if is_admin(request.user):
        return redirect("admin-dashboard")
    elif is_teacher(request.user):
        accountapproval = models.Teacher.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect("teacher-dashboard")
        else:
            return render(request, "college/teacher_approval_pending.html")
    elif is_student(request.user):
        accountapproval = models.Student.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect("student-dashboard")
        else:
            return render(request, "college/student_approval_pending.html")


# Admin dashboard
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_dashboard(request):
    teachercount = models.Teacher.objects.all().filter(status=True).count()
    pendingteachercount = models.Teacher.objects.all().filter(status=False).count()

    studentcount = models.Student.objects.all().filter(status=True).count()
    pendingstudentcount = models.Student.objects.all().filter(status=False).count()

    teachersalary = models.Teacher.objects.filter(status=True).aggregate(
        Sum("salary", default=0)
    )

    studentfee = models.Student.objects.filter(status=True).aggregate(
        Sum("fee", default=0)
    )

    notice = models.Notice.objects.all()
    complain = models.Complain.objects.all()
    leave = models.Leave.objects.all()

    # aggregate function returns dictionary so fetch data from dictionay
    mydict = {
        "teachercount": teachercount,
        "pendingteachercount": pendingteachercount,
        "studentcount": studentcount,
        "pendingstudentcount": pendingstudentcount,
        "teachersalary": teachersalary["salary__sum"],
        "studentfee": studentfee["fee__sum"],
        "notice": notice,
        "complain":complain,
        "leave":leave,
    }

    return render(request, "college/admin_dashboard.html", context=mydict)


# teacher section in admin panel
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_teacher_section(request):
    return render(request, "college/admin_teacher_section.html")


# Add teacher by admin
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_teacher(request):
    form1 = forms.TeacherUserForm()
    form2 = forms.TeacherFormAdditional()
    mydict = {"form1": form1, "form2": form2}
    if request.method == "POST":
        form1 = forms.TeacherUserForm(request.POST)
        form2 = forms.TeacherFormAdditional(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            f2 = form2.save(commit=False)
            f2.user = user
            f2.status = True
            f2.save()

            teacher_group = Group.objects.get_or_create(name="TEACHER")
            teacher_group[0].user_set.add(user)

        return HttpResponseRedirect("admin-teacher")
    return render(request, "college/admin_add_teacher.html", context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher(request):
    teachers=models.Teacher.objects.all().filter(status=True)
    return render(request,'college/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_teacher(request):
    teachers=models.Teacher.objects.all().filter(status=False)
    return render(request,'college/admin_approve_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_teacher(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    teacher.status=True
    teacher.save()
    return redirect('admin-approve-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def disapprove_teacher(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-approve-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-view-teacher')


# student section in admin panel
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_student_section(request):
    return render(request, "college/admin_student_section.html")


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentFormAdditional()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentFormAdditional(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            student_group = Group.objects.get_or_create(name='STUDENT')
            student_group[0].user_set.add(user)
        return HttpResponseRedirect('admin-student')
    return render(request,'college/admin_add_student.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student(request):
    students=models.Student.objects.all().filter(status=True)
    return render(request,'college/admin_view_student.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student(request):
    students=models.Student.objects.all().filter(status=False)
    return render(request,'college/admin_approve_student.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student(request,pk):
    students=models.Student.objects.get(id=pk)
    students.status=True
    students.save()
    return redirect('admin-approve-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def disapprove_student(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-approve-student')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')


# notice by admin
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notice(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('admin-dashboard')
    return render(request,'college/admin_notice.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_delete_notice(request,pk):
    notice=models.Notice.objects.get(id=pk)
    notice.delete()
    return redirect('admin-dashboard')


# teacher dashboard
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacherdata=models.Teacher.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    leave=models.Leave.objects.all()
    mydict={
        'salary':teacherdata[0].salary,
        'address':teacherdata[0].address,
        'phone_no':teacherdata[0].phone_no,
        'date':teacherdata[0].joindate,
        'notice':notice,
        'leave':leave,
        
    }
    return render(request,'college/teacher_dashboard.html',context=mydict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def update_teacher(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)

    form1=forms.TeacherUserForm(instance=user)
    form2=forms.TeacherFormAdditional(instance=teacher)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST,instance=user)
        form2=forms.TeacherFormAdditional(request.POST,instance=teacher)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('teacher-dashboard')
    return render(request,'college/update_teacher.html',context=mydict)

#notice by teacher
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_notice(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('teacher-dashboard')
    return render(request,'college/teacher_notice.html',{'form':form})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_leave(request):
    form=forms.LeaveForm()
    if request.method=='POST':
        form=forms.LeaveForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('teacher-dashboard')
    return render(request,'college/teacher_leave.html',{'form':form})

# teacher attendance view
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_attendance(request):
    return render(request,'college/teacher_attendance.html')

# teacher take attendance
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def take_attendance(request,faculty):
    students=models.Student.objects.all().filter(faculty=faculty)
    attendanceform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.faculty=faculty
                AttendanceModel.date=date
                AttendanceModel.present=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('teacher-attendance')
    return render(request,'college/take_attendance.html',{'students':students,'attendanceform':attendanceform})

# teacher view attendance
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def view_attendance(request,faculty):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(faculty=faculty,date=date)
            studentdata=models.Student.objects.all().filter(faculty=faculty)
            attendance_list=zip(attendancedata,studentdata)
            return render(request,'college/view_attendance.html',{'attendance_list':attendance_list,'faculty':faculty,'date':date})
    return render(request,'college/view_attendance_date.html',{'faculty':faculty,'form':form})


# for student dashboard
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard(request):
    studentdata=models.Student.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    complain = models.Complain.objects.all()
    mydict={
        'roll':studentdata[0].roll,
        'faculty':studentdata[0].faculty,
        'address':studentdata[0].address,
        'phone_no':studentdata[0].phone_no,
        'fee':studentdata[0].fee,
        'notice':notice,
        'complain':complain
    }
    return render(request,'college/student_dashboard.html',context=mydict)


# complain by student
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_complain(request):
    form=forms.ComplainForm()
    if request.method=='POST':
        form=forms.ComplainForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('student-dashboard')
    return render(request,'college/student_complain.html',{'form':form})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def update_student(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentFormAdditional(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentFormAdditional(request.POST,instance=student)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('student-dashboard')
    return render(request,'college/update_student.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_resolve_complain(request,pk):
    complain=models.Complain.objects.get(id=pk)
    complain.delete()
    return redirect('admin-dashboard')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_teacher_leave(request,pk):
    leave=models.Leave.objects.get(id=pk)
    leave.delete()
    return redirect('admin-dashboard')
