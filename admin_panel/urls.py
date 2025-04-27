# admin_panel/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='admin_panel/login.html'), name='admin_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='admin_login'), name='admin_logout'),
    
    # Celebrity management
    path('celebrities/', views.celebrity_list, name='admin_celebrity_list'),
    path('celebrities/add/', views.add_celebrity, name='admin_add_celebrity'),
    path('celebrities/edit/<int:celebrity_id>/', views.edit_celebrity, name='admin_edit_celebrity'),
    path('celebrities/delete/<int:celebrity_id>/', views.delete_celebrity, name='admin_delete_celebrity'),
    
    # Reservation management
    path('reservations/', views.reservation_list, name='admin_reservation_list'),
    path('reservations/<int:reservation_id>/', views.reservation_detail, name='admin_reservation_detail'),
    path('reservations/<int:reservation_id>/update-status/', views.update_reservation_status, name='admin_update_reservation_status'),
    
    # Email functionality
    path('send-email/', views.send_email, name='admin_send_email'),
    path('send-email/<int:reservation_id>/', views.send_email, name='admin_send_email_to_reservation'),
]