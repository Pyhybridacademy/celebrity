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
    
    # Payment Method management
    path('payment-methods/', views.payment_method_list, name='admin_payment_method_list'),
    path('payment-methods/add/', views.add_payment_method, name='admin_add_payment_method'),
    path('payment-methods/edit/<int:payment_method_id>/', views.edit_payment_method, name='admin_edit_payment_method'),
    path('payment-methods/delete/<int:payment_method_id>/', views.delete_payment_method, name='admin_delete_payment_method'),
    
    # Crypto Wallet management
    path('crypto-wallets/', views.crypto_wallet_list, name='admin_crypto_wallet_list'),
    path('crypto-wallets/add/', views.add_crypto_wallet, name='admin_add_crypto_wallet'),
    path('crypto-wallets/edit/<int:wallet_id>/', views.edit_crypto_wallet, name='admin_edit_crypto_wallet'),
    path('crypto-wallets/delete/<int:wallet_id>/', views.delete_crypto_wallet, name='admin_delete_crypto_wallet'),
    
    # Membership Tier management
    path('membership-tiers/', views.membership_tier_list, name='admin_membership_tier_list'),
    path('membership-tiers/add/', views.add_membership_tier, name='admin_add_membership_tier'),
    path('membership-tiers/edit/<int:tier_id>/', views.edit_membership_tier, name='admin_edit_membership_tier'),
    path('membership-tiers/delete/<int:tier_id>/', views.delete_membership_tier, name='admin_delete_membership_tier'),
    
    # Membership Application management
    path('membership-applications/', views.membership_application_list, name='admin_membership_application_list'),
    path('membership-applications/<int:application_id>/', views.membership_application_detail, name='admin_membership_application_detail'),
    path('membership-applications/<int:application_id>/update-status/', views.update_membership_application_status, name='admin_update_membership_application_status'),
    
    # Charity Donation management
    path('charity-donations/', views.charity_donation_list, name='admin_charity_donation_list'),
    path('charity-donations/<int:donation_id>/', views.charity_donation_detail, name='admin_charity_donation_detail'),
    path('charity-donations/<int:donation_id>/update-status/', views.update_charity_donation_status, name='admin_update_charity_donation_status'),
    
    # Modeling Contract management
    path('modeling-contracts/', views.modeling_contract_list, name='admin_modeling_contract_list'),
    path('modeling-contracts/<int:contract_id>/', views.modeling_contract_detail, name='admin_modeling_contract_detail'),
    path('modeling-contracts/<int:contract_id>/update-status/', views.update_modeling_contract_status, name='admin_update_modeling_contract_status'),
    
    # Brand Ambassador management
    path('brand-ambassadors/', views.brand_ambassador_list, name='admin_brand_ambassador_list'),
    path('brand-ambassadors/<int:ambassador_id>/', views.brand_ambassador_detail, name='admin_brand_ambassador_detail'),
    path('brand-ambassadors/<int:ambassador_id>/update-status/', views.update_brand_ambassador_status, name='admin_update_brand_ambassador_status'),
    
    # Site Settings
    path('site-settings/', views.site_settings, name='admin_site_settings'),
    
    # Email functionality
    path('send-email/', views.send_email, name='admin_send_email'),
    path('send-email/<int:reservation_id>/', views.send_email, name='admin_send_email_to_reservation'),
    path('send-email-applicant/<int:application_id>/', views.send_email_to_applicant, name='admin_send_email_to_applicant'),
    path('send-email-donor/<int:donation_id>/', views.send_email_to_donor, name='admin_send_email_to_donor'),
    path('send-email-contract/<int:contract_id>/', views.send_email_to_contract_applicant, name='admin_send_email_to_contract'),
    path('send-email-ambassador/<int:ambassador_id>/', views.send_email_to_ambassador, name='admin_send_email_to_ambassador'),
]