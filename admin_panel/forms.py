# admin_panel/forms.py
from django import forms
from main.models import Celebrity

class CelebrityForm(forms.ModelForm):
    class Meta:
        model = Celebrity
        fields = ['name', 'bio', 'image', 'hourly_rate', 'available']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
        }

class EmailForm(forms.Form):
    recipient_email = forms.EmailField(label='Recipient Email')
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))