# main/forms.py
from django import forms
from .models import Reservation
from django.utils import timezone
import datetime

class ReservationForm(forms.ModelForm):
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()}),
    )
    booking_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )
    
    class Meta:
        model = Reservation
        fields = ['user_name', 'user_email', 'phone_number', 'booking_date', 
                  'booking_time', 'duration_hours', 'message']
        
    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        today = timezone.now().date()
        
        if booking_date < today:
            raise forms.ValidationError("Booking date cannot be in the past.")
        
        return booking_date