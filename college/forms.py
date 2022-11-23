from django import forms
from django.contrib.auth.models import User
from college import models


# signup form for admin 
class AdminSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['first_name','last_name','username','password']
        
# teacher signup form
class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class TeacherFormAdditional(forms.ModelForm):
    class Meta:
        model=models.Teacher
        fields=['salary','phone_no','address','status'] 
        
# student signup form
class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class StudentFormAdditional(forms.ModelForm):
    class Meta:
        model=models.Student
        fields=['roll','faculty','phone_no','address','fee','status']
    

# notice related form
class NoticeForm(forms.ModelForm):
    class Meta:
        model = models.Notice
        fields = '__all__'
        

# attendance related form 
attendance_choices = (('Present','Present'),('Absent','Absent'))
class AttendanceForm(forms.Form):
    present = forms.ChoiceField(choices=attendance_choices)
    date = forms.DateField()
    
class AskDateForm(forms.Form):
    date = forms.DateField()
    
    
# complain related form
class ComplainForm(forms.ModelForm):
    class Meta:
        model = models.Complain
        fields = '__all__'
        
        
# complain related form
class LeaveForm(forms.ModelForm):
    class Meta:
        model = models.Leave
        fields = '__all__'