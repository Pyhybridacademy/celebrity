from django.contrib import admin
from .models import (
    Celebrity, Reservation, PaymentMethod, CryptoWallet, 
    MembershipTier, MembershipApplication, CharityDonation
)

@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    list_display = ('name', 'hourly_rate', 'available', 'created_at')
    list_filter = ('available', 'created_at')
    search_fields = ('name', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'bio', 'image')
        }),
        ('Booking Details', {
            'fields': ('hourly_rate', 'available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'celebrity', 'booking_date', 'booking_time', 'status', 'created_at')
    list_filter = ('status', 'booking_date', 'created_at')
    search_fields = ('user_name', 'user_email', 'celebrity__name')
    readonly_fields = ('created_at', 'updated_at', 'total_cost')
    fieldsets = (
        ('Customer Information', {
            'fields': ('user_name', 'user_email', 'phone_number')
        }),
        ('Booking Details', {
            'fields': ('celebrity', 'booking_date', 'booking_time', 'duration_hours', 'status')
        }),
        ('Additional Information', {
            'fields': ('message', 'total_cost')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
        
    def total_cost(self, obj):
        return f"${obj.total_cost}"
    total_cost.short_description = "Total Cost"

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ('currency', 'wallet_address', 'is_active')
    list_filter = ('currency', 'is_active')
    search_fields = ('currency', 'wallet_address')

@admin.register(MembershipTier)
class MembershipTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')
    search_fields = ('name',)

@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'tier', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'tier', 'created_at')
    search_fields = ('full_name', 'email', 'payment_details')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Applicant Information', {
            'fields': ('full_name', 'email', 'phone_number', 'address')
        }),
        ('Membership Details', {
            'fields': ('tier', 'status')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_details', 'payment_proof')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CharityDonation)
class CharityDonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at', 'anonymous')
    search_fields = ('donor_name', 'donor_email', 'payment_details')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'anonymous')
        }),
        ('Donation Details', {
            'fields': ('amount', 'message', 'status')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_details', 'payment_proof')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
