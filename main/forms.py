from django import forms
from .models import Reservation, ModelingContract, BrandAmbassador, SiteSettings, ContactMessage, MembershipApplication, CharityDonation, MembershipTier
from django.utils import timezone

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

class ModelingContractForm(forms.ModelForm):
    class Meta:
        model = ModelingContract
        fields = ['full_name', 'email', 'phone_number', 'portfolio', 
                  'payment_method', 'payment_proof', 'payment_details', 'amount']
        widgets = {
            'portfolio': forms.Textarea(attrs={'rows': 3}),
            'payment_details': forms.Textarea(attrs={'rows': 3}),
        }

class BrandAmbassadorForm(forms.ModelForm):
    class Meta:
        model = BrandAmbassador
        fields = ['full_name', 'email', 'phone_number', 'social_media', 
                  'payment_method', 'payment_proof', 'payment_details', 'amount']
        widgets = {
            'social_media': forms.Textarea(attrs={'rows': 3}),
            'payment_details': forms.Textarea(attrs={'rows': 3}),
        }

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['site_name', 'logo', 'contact_email', 'address', 'phone_number', 'Telegram']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }