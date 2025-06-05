from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('celebrity/<int:celebrity_id>/', views.celebrity_detail, name='celebrity_detail'),
    path('celebrity/', views.celebrity_list, name='celebrity_list'),
    path('book/<int:celebrity_id>/', views.book_reservation, name='book_reservation'),
    path('confirmation/<int:reservation_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('membership/', views.membership_info, name='membership_info'),
    path('membership/apply/', views.apply_membership, name='apply_membership'),
    path('membership/confirmation/<int:application_id>/', views.membership_confirmation, name='membership_confirmation'),
    path('donate/', views.donate_charity, name='donate_charity'),
    path('donate/confirmation/<int:donation_id>/', views.donation_confirmation, name='donation_confirmation'),
    path('donate/list/', views.donation_list, name='donation_list'),
    path('modeling-contract/apply/', views.apply_modeling_contract, name='apply_modeling_contract'),
    path('modeling-contract/confirmation/<int:contract_id>/', views.modeling_contract_confirmation, name='modeling_contract_confirmation'),
    path('brand-ambassador/apply/', views.apply_brand_ambassador, name='apply_brand_ambassador'),
    path('brand-ambassador/confirmation/<int:ambassador_id>/', views.brand_ambassador_confirmation, name='brand_ambassador_confirmation'),
]