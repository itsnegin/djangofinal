from django.urls import path
from . import views

app_name = 'sematec'

urlpatterns = [
    path('', views.course_list_view, name='course_list'),
    path('add/', views.course_create_view, name='course_create'),
    path('<int:pk>/', views.course_detail_view, name='course_detail'),
    path('<int:pk>/edit/', views.course_edit_view, name='course_edit'),
    path('<int:pk>/delete/', views.course_delete_view, name='course_delete'),
    path('<int:pk>/enroll/', views.course_enroll_view, name='course_enroll'),
    path('lessons/<int:pk>/', views.lesson_detail_view, name='lesson_detail'),
    path('lessons/<int:pk>/complete/', views.lesson_complete_view, name='lesson_complete'),
    path('instructors/<int:pk>/', views.instructor_detail_view, name='instructor_detail'),
    path('course/<int:pk>/lessons/', views.course_lessons_view, name='course_lessons'),
]