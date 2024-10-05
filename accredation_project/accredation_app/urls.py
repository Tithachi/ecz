# accredation_app/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout as auth_logout
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('application/', application_form, name='application_form'),
    path('application_lo/', application_lo_form, name='application_lo_form'),
    path('application_success/', application_success, name='application_success'),
    path('manage_applications/', manage_applications, name='manage_applications'),
    # path('approve_application/<int:application_id>/', approve_application, name='approve_application'),
    path('reject_application/<int:application_id>/', reject_application, name='reject_application'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    # path('download_certificate/<int:application_id>/', download_certificate, name='download_certificate'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('application/<int:application_id>/', views.view_application, name='view_application'),
    path('approve_application/<int:application_id>/', views.approve_application, name='approve_application'),
    # path('download_application/<int:application_id>/', views.download_application, name='download_application'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)