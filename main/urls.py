# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('celebrity/<int:celebrity_id>/', views.celebrity_detail, name='celebrity_detail'),
    path('book/<int:celebrity_id>/', views.book_reservation, name='book_reservation'),
    path('confirmation/<int:reservation_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]