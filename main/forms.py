# main/forms.py
from django import forms
from .models import Reservation
from django.utils import timezone
import datetime
from django import forms
from .models import MembershipApplication, CharityDonation, MembershipTier

class MembershipApplicationForm(forms.ModelForm):
    class Meta:
        model = MembershipApplication
        fields = ['tier', 'full_name', 'email', 'phone_number', 'address', 
                  'payment_method', 'payment_proof', 'payment_details']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'payment_details': forms.Textarea(attrs={'rows': 3}),
        }

class CharityDonationForm(forms.ModelForm):
    class Meta:
        model = CharityDonation
        fields = ['donor_name', 'donor_email', 'amount', 'payment_method', 
                  'payment_proof', 'payment_details', 'message', 'anonymous']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
            'payment_details': forms.Textarea(attrs={'rows': 3}),
        }

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