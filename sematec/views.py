
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Count, F
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import (
    Category,
    Course,
    Enrollment,
    Instructor,
    InstructorProfile,
    Lesson,
    LessonProgress,
    StudentProfile
)

from .forms import (
    NewCourseForm,
    UserInfoForm,
    StudentProfileForm,
    TeacherForm,
    InstructorProfileForm,
    AddStudentForm,
)


# =========================
# HOME
# =========================

def home_view(request):
    courses = Course.objects.all().order_by('-date_created')[:3]

    return render(request, 'home.html', {
        'courses': courses
    })


# =========================
# COURSES
# =========================

def course_list_view(request):
    courses = Course.objects.select_related(
        'category'
    ).order_by('-date_created')

    categories = Category.objects.all()
    selected = request.GET.get('category', '')

    if selected.isdigit():
        courses = courses.filter(category_id=int(selected))

    return render(request, 'course/course_list.html', {
        'courses': courses,
        'categories': categories,
        'selected': selected,
        'current_language': request.LANGUAGE_CODE,
    })


def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    is_enrolled = False

    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()

    return render(request, 'course/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled
    })


@staff_member_required
def course_create_view(request):
    if request.method == 'POST':
        form = NewCourseForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('sematec:course_list')
    else:
        form = NewCourseForm()

    return render(request, 'course/course_form.html', {
        'form': form
    })


@staff_member_required
def course_edit_view(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = NewCourseForm(
            request.POST,
            request.FILES,
            instance=course
        )

        if form.is_valid():
            form.save()
            return redirect('sematec:course_detail', pk=course.pk)
    else:
        form = NewCourseForm(instance=course)

    return render(request, 'course/course_form.html', {
        'form': form,
        'course': course
    })


@staff_member_required
def course_delete_view(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        course.delete()
        return redirect('sematec:course_list')

    return render(request, 'course/course_confirm_delete.html', {
        'course': course
    })


@login_required
def course_enroll_view(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST' and not course.is_full:
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            course=course
        )

        if created:
            course.enrolled_count = F('enrolled_count') + 1
            course.save(update_fields=['enrolled_count'])

    return redirect('dashboard')


# =========================
# LESSONS
# =========================

@login_required
def course_lessons_view(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if not Enrollment.objects.filter(
        user=request.user,
        course=course
    ).exists():
        return redirect('sematec:course_detail', pk=course.pk)

    lessons = course.lessons.all()

    return render(request, 'course/lessons.html', {
        'course': course,
        'lessons': lessons,
    })


@login_required
def lesson_detail_view(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if not Enrollment.objects.filter(
        user=request.user,
        course=lesson.course
    ).exists():
        return redirect('sematec:course_detail', pk=lesson.course.pk)

    is_completed = LessonProgress.objects.filter(
        user=request.user,
        lesson=lesson
    ).exists()

    return render(request, 'course/lesson_detail.html', {
        'lesson': lesson,
        'is_completed': is_completed
    })


@login_required
def lesson_complete_view(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == 'POST' and Enrollment.objects.filter(
        user=request.user,
        course=lesson.course
    ).exists():
        LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )

    return redirect('sematec:lesson_detail', pk=lesson.pk)


# =========================
# INSTRUCTORS
# =========================

def instructor_detail_view(request, pk):
    instructor = get_object_or_404(
        Instructor.objects.select_related('profile'),
        pk=pk
    )

    courses = instructor.courses.select_related(
        'category'
    ).order_by('-date_created')

    return render(request, 'course/instructor_detail.html', {
        'instructor': instructor,
        'courses': courses,
        'profile': getattr(instructor, 'profile', None),
    })


# =========================
# AUTHENTICATION
# =========================

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')

    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {
        'form': form
    })


def logout_view(request):
    if request.method == 'POST':
        logout(request)

    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


# =========================
# STUDENT DASHBOARD
# =========================

@login_required
def dashboard_view(request):
    enrollments = list(
        Enrollment.objects.filter(
            user=request.user
        ).select_related('course').order_by('-date_enrolled')
    )

    for enrollment in enrollments:
        total = enrollment.course.lessons.count()

        done = LessonProgress.objects.filter(
            user=request.user,
            lesson__course=enrollment.course
        ).count()

        enrollment.total_lessons = total
        enrollment.done_lessons = done
        enrollment.progress = int(done * 100 / total) if total else 0

    return render(request, 'accounts/dashboard.html', {
        'enrollments': enrollments
    })


@login_required
def profile_view(request):
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        user_form = UserInfoForm(
            request.POST,
            instance=request.user
        )

        profile_form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, _('Your profile was saved.'))
            return redirect('profile')
    else:
        user_form = UserInfoForm(instance=request.user)
        profile_form = StudentProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


# =========================
# ADMIN DASHBOARD
# =========================

@staff_member_required
def manage_dashboard_view(request):
    User = get_user_model()

    stats = {
        'students': User.objects.filter(is_staff=False).count(),
        'courses': Course.objects.count(),
        'enrollments': Enrollment.objects.count(),
        'instructors': Instructor.objects.count(),
        'categories': Category.objects.count(),
        'lessons': Lesson.objects.count(),
    }

    latest_enrollments = Enrollment.objects.select_related(
        'user',
        'course'
    ).order_by('-date_enrolled')[:5]

    return render(request, 'manage/dashboard.html', {
        'stats': stats,
        'latest_enrollments': latest_enrollments
    })


# =========================
# STUDENTS MANAGEMENT
# =========================

@staff_member_required
def students_list_view(request):
    User = get_user_model()

    students = (
        User.objects.filter(is_staff=False)
        .select_related('profile')
        .annotate(enrollments_count=Count('enrollments'))
        .order_by('-date_joined')
    )

    for student in students:
        student.display_name = (
            student.profile.name_fa
            if request.LANGUAGE_CODE == 'fa'
            and hasattr(student, 'profile')
            and student.profile.name_fa
            else student.get_full_name() or student.username
        )

    return render(request, 'manage/students_list.html', {
        'students': students,
        'current_language': request.LANGUAGE_CODE,
    })


@staff_member_required
def student_detail_view(request, pk):
    User = get_user_model()

    student = get_object_or_404(
        User,
        pk=pk,
        is_staff=False
    )

    profile = StudentProfile.objects.filter(
        user=student
    ).first()

    enrollments = list(
        Enrollment.objects.filter(
            user=student
        ).select_related('course').order_by('-date_enrolled')
    )

    for enrollment in enrollments:
        total = enrollment.course.lessons.count()

        done = LessonProgress.objects.filter(
            user=student,
            lesson__course=enrollment.course
        ).count()

        enrollment.total_lessons = total
        enrollment.done_lessons = done
        enrollment.progress = int(done * 100 / total) if total else 0

    return render(request, 'manage/student_detail.html', {
        'student': student,
        'profile': profile,
        'enrollments': enrollments,
    })


@staff_member_required
def student_create_view(request):
    User = get_user_model()

    if request.method == 'POST':
        user_form = AddStudentForm(request.POST)
        profile_form = StudentProfileForm(
            request.POST,
            request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            data = user_form.cleaned_data

            user = User.objects.create_user(
                username=data['username'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
            )

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, _('Student was added.'))
            return redirect('students')
    else:
        user_form = AddStudentForm()
        profile_form = StudentProfileForm()

    return render(request, 'manage/student_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@staff_member_required
def student_edit_view(request, pk):
    User = get_user_model()

    student = get_object_or_404(
        User,
        pk=pk,
        is_staff=False
    )

    profile, created = StudentProfile.objects.get_or_create(
        user=student
    )

    if request.method == 'POST':
        user_form = UserInfoForm(
            request.POST,
            instance=student
        )

        profile_form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, _('Student was updated.'))
            return redirect('students')
    else:
        user_form = UserInfoForm(instance=student)
        profile_form = StudentProfileForm(instance=profile)

    return render(request, 'manage/student_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'student': student,
    })


@staff_member_required
def student_delete_view(request, pk):
    User = get_user_model()

    student = get_object_or_404(
        User,
        pk=pk,
        is_staff=False
    )

    if request.method == 'POST':
        student.delete()
        messages.success(request, _('Student was deleted.'))
        return redirect('students')

    return render(request, 'manage/student_confirm_delete.html', {
        'student': student
    })


# =========================
# TEACHERS MANAGEMENT
# =========================

@staff_member_required
def teachers_list_view(request):
    teachers = Instructor.objects.select_related(
        'profile'
    ).prefetch_related(
        'courses'
    ).order_by('name')

    for teacher in teachers:
        teacher.display_name = (
            teacher.name_fa
            if request.LANGUAGE_CODE == 'fa' and teacher.name_fa
            else teacher.name
        )

        teacher.teacher_profile = getattr(
            teacher,
            'profile',
            None
        )

    return render(request, 'manage/teachers_list.html', {
        'teachers': teachers,
        'current_language': request.LANGUAGE_CODE,
    })


@staff_member_required
def teacher_create_view(request):
    if request.method == 'POST':
        form = TeacherForm(
            request.POST,
            request.FILES
        )

        profile_form = InstructorProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            teacher = form.save()

            profile = profile_form.save(commit=False)
            profile.instructor = teacher
            profile.save()

            messages.success(request, _('Teacher was added.'))
            return redirect('teachers')
    else:
        form = TeacherForm()
        profile_form = InstructorProfileForm()

    return render(request, 'manage/teacher_form.html', {
        'form': form,
        'profile_form': profile_form,
    })


@staff_member_required
def teacher_edit_view(request, pk):
    teacher = get_object_or_404(
        Instructor.objects.select_related('profile'),
        pk=pk
    )

    profile, created = InstructorProfile.objects.get_or_create(
        instructor=teacher
    )

    if request.method == 'POST':
        form = TeacherForm(
            request.POST,
            request.FILES,
            instance=teacher
        )

        profile_form = InstructorProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()

            messages.success(request, _('Teacher was updated.'))
            return redirect('teachers')
    else:
        form = TeacherForm(instance=teacher)
        profile_form = InstructorProfileForm(instance=profile)

    return render(request, 'manage/teacher_form.html', {
        'form': form,
        'profile_form': profile_form,
        'teacher': teacher,
    })


@staff_member_required
def teacher_delete_view(request, pk):
    teacher = get_object_or_404(Instructor, pk=pk)

    if request.method == 'POST':
        teacher.delete()
        messages.success(request, _('Teacher was deleted.'))
        return redirect('teachers')

    return render(request, 'manage/teacher_confirm_delete.html', {
        'teacher': teacher
    })