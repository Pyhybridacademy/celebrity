from django import forms
from main.models import (
    Celebrity, Reservation, PaymentMethod, CryptoWallet, 
    MembershipTier, MembershipApplication, CharityDonation,
    ModelingContract, BrandAmbassador, SiteSettings
)

class CelebrityForm(forms.ModelForm):
    class Meta:
        model = Celebrity
        fields = ['name', 'bio', 'image', 'hourly_rate', 'available']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['celebrity', 'user_name', 'user_email', 'phone_number', 
                 'booking_date', 'booking_time', 'duration_hours', 'message', 'status']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['name', 'description', 'instructions', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }

class CryptoWalletForm(forms.ModelForm):
    class Meta:
        model = CryptoWallet
        fields = ['currency', 'wallet_address', 'qr_code', 'is_active']

class MembershipTierForm(forms.ModelForm):
    class Meta:
        model = MembershipTier
        fields = ['name', 'price', 'duration_days', 'description', 'benefits']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'benefits': forms.Textarea(attrs={'rows': 3}),
        }

class MembershipApplicationForm(forms.ModelForm):
    class Meta:
        model = MembershipApplication
        fields = ['tier', 'full_name', 'email', 'phone_number', 'address',
                 'payment_method', 'payment_proof', 'payment_details', 'status']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'payment_details': forms.Textarea(attrs={'rows': 3}),
        }

class CharityDonationForm(forms.ModelForm):
    class Meta:
        model = CharityDonation
        fields = ['donor_name', 'donor_email', 'amount', 'payment_method',
                 'payment_proof', 'payment_details', 'message', 'status', 'anonymous']
        widgets = {
            'payment_details': forms.Textarea(attrs={'rows': 3}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }

class ModelingContractForm(forms.ModelForm):
    class Meta:
        model = ModelingContract
        fields = ['full_name', 'email', 'phone_number', 'portfolio', 
                  'payment_method', 'payment_proof', 'payment_details', 'amount', 'status']
        widgets = {
            'portfolio': forms.Textarea(attrs={'rows': 3}),
            'payment_details': forms.Textarea(attrs={'rows': 3}),
        }

class BrandAmbassadorForm(forms.ModelForm):
    class Meta:
        model = BrandAmbassador
        fields = ['full_name', 'email', 'phone_number', 'social_media', 
                  'payment_method', 'payment_proof', 'payment_details', 'amount', 'status']
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

class EmailForm(forms.Form):
    recipient_email = forms.EmailField(label="Recipient Email")
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))