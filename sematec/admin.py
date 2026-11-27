from django.contrib import admin
from .models import (
    Category,
    Course,
    Enrollment,
    Instructor,
    InstructorProfile,
    Lesson,
    StudentProfile,
)
@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'instructor',
        'national_code',
        'birth_date',
        'gender',
        'education',
        'city',
        'phone',
        'email',
    )
search_fields = (
    'instructor__name',
    'instructor__name_fa',
    'national_code',
    'phone',
    'email',
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name',)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'instructor',
        'duration',
        'teacher',
        'capacity',
        'price',
    )
    ordering = ('-date_created',)
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'date_enrolled')
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name_fa', 'phone', 'city')
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'name_fa',
    )