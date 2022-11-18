from django.contrib import admin
from college.models import *

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    pass

class TeacherAdmin(admin.ModelAdmin):
    pass


admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher,TeacherAdmin)
