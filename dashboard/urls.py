from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import ProjectViewSet, TaskViewSet

urlpatterns = [
    # Authentication views
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),  # Use custom login view
    path('logout/', views.logout_view, name='logout'),  # Custom logout view

    # Dashboard and Profile views
    path('', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),

    # Project and Task views
    path('projects/', views.project_list, name='project_list'),  # Corrected to match view name
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project'),
    
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    
    path('progress-report/', views.progress_report_view, name='progress_report'), 
]

# API routes
router = DefaultRouter()
router.register('api/projects', ProjectViewSet)
router.register('api/tasks', TaskViewSet)

# Append API URLs
urlpatterns += router.urls
