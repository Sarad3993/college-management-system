from django.contrib import admin
from college.models import *

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    pass

class TeacherAdmin(admin.ModelAdmin):
    pass

class NoticeAdmin(admin.ModelAdmin):
    pass

class AttendanceAdmin(admin.ModelAdmin):
    pass

class ComplainAdmin(admin.ModelAdmin):
    pass

class LeaveAdmin(admin.ModelAdmin):
    pass


admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Notice,NoticeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Complain, ComplainAdmin)
admin.site.register(Leave,LeaveAdmin)
