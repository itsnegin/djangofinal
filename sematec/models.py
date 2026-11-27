
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_fa = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        from django.utils.translation import get_language
        if get_language() == 'fa' and self.name_fa:
            return self.name_fa
        return self.name


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    name_fa = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    bio_fa = models.TextField(blank=True)
    photo = models.ImageField(upload_to='instructors/', blank=True)

    def __str__(self):
        from django.utils.translation import get_language
        if get_language() == 'fa' and self.name_fa:
            return self.name_fa
        return self.name


class InstructorProfile(models.Model):
    instructor = models.OneToOneField(
        Instructor,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    national_code = models.CharField(max_length=10, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', _('Male')),
            ('female', _('Female')),
        ],
        blank=True
    )

    education = models.CharField(
        max_length=20,
        choices=[
            ('diploma', _('Diploma')),
            ('associate', _('Associate degree')),
            ('bachelor', _('Bachelor')),
            ('master', _('Master')),
            ('phd', _('PhD')),
            ('other', _('Other')),
        ],
        blank=True
    )

    city = models.CharField(max_length=100, blank=True)
    city_fa = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f'{self.instructor.name} - Profile'


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
        ('comprehensive', _('Comprehensive')),
    ]

    title = models.CharField(max_length=100)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )

    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )

    description = models.TextField()
    description_fa = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    teacher = models.CharField(max_length=70)
    price = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='beginner'
    )
    certificate = models.BooleanField(default=False)
    prerequisites = models.TextField()
    capacity = models.PositiveIntegerField()
    enrolled_count = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='courses/', blank=True)

    def __str__(self):
        return self.title

    def clean(self):
        if (
            self.capacity is not None
            and self.enrolled_count is not None
            and self.enrolled_count > self.capacity
        ):
            raise ValidationError('enrolled count cannot exceed capacity!')

    @property
    def remaining_capacity(self):
        return self.capacity - self.enrolled_count

    @property
    def is_full(self):
        return self.enrolled_count >= self.capacity


class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='unique_user_course'
            ),
        ]

    def __str__(self):
        return f'{self.user} - {self.course}'


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    content = models.TextField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class LessonProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lesson_progress'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress'
    )
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'lesson'],
                name='unique_user_lesson'
            ),
        ]

    def __str__(self):
        return f'{self.user} - {self.lesson}'


class StudentProfile(models.Model):
    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
    ]

    EDUCATION_CHOICES = [
        ('diploma', _('Diploma')),
        ('associate', _('Associate degree')),
        ('bachelor', _('Bachelor')),
        ('master', _('Master')),
        ('phd', _('PhD')),
        ('other', _('Other')),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    name_fa = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to='students/', blank=True)
    father_name = models.CharField(max_length=100, blank=True)
    national_code = models.CharField(max_length=10, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True
    )
    education = models.CharField(
        max_length=20,
        choices=EDUCATION_CHOICES,
        blank=True
    )
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    city_fa = models.CharField(max_length=100, blank=True)

    def __str__(self):
        from django.utils.translation import get_language

        if get_language() == 'fa' and self.name_fa:
            return self.name_fa

        return self.user.get_full_name() or self.user.username