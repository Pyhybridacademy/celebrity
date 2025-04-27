# main/admin.py
from django.contrib import admin
from .models import Celebrity, Reservation

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