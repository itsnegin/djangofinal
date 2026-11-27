from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from sematec import views as sematec_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

# Courses
path('courses/', include('sematec.urls')),

# Authentication
path('', sematec_views.login_view, name='login'),
path('login/', sematec_views.login_view, name='login_page'),
path('logout/', sematec_views.logout_view, name='logout'),
path('register/', sematec_views.register_view, name='register'),

# Home and student pages
path('home/', sematec_views.home_view, name='home'),
path('dashboard/', sematec_views.dashboard_view, name='dashboard'),
path('profile/', sematec_views.profile_view, name='profile'),

# Management
path('manage/', sematec_views.manage_dashboard_view, name='manage_dashboard'),

path('manage/students/', sematec_views.students_list_view, name='students'),
path('manage/students/add/', sematec_views.student_create_view, name='student_create'),
path('manage/students/<int:pk>/', sematec_views.student_detail_view, name='student_detail'),
path('manage/students/<int:pk>/edit/', sematec_views.student_edit_view, name='student_edit'),
path('manage/students/<int:pk>/delete/', sematec_views.student_delete_view, name='student_delete'),

path('manage/teachers/', sematec_views.teachers_list_view, name='teachers'),
path('manage/teachers/add/', sematec_views.teacher_create_view, name='teacher_create'),
path('manage/teachers/<int:pk>/edit/', sematec_views.teacher_edit_view, name='teacher_edit'),
path('manage/teachers/<int:pk>/delete/', sematec_views.teacher_delete_view, name='teacher_delete'),
]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)