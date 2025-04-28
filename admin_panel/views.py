# admin_panel/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings
from django.db.models import Sum
from main.models import (
    Celebrity, Reservation, PaymentMethod, CryptoWallet, 
    MembershipTier, MembershipApplication, CharityDonation
)
from .forms import (
    CelebrityForm, ReservationForm, PaymentMethodForm, CryptoWalletForm,
    MembershipTierForm, MembershipApplicationForm, CharityDonationForm, EmailForm
)

@login_required
def admin_dashboard(request):
    celebrities_count = Celebrity.objects.count()
    reservations_count = Reservation.objects.count()
    pending_reservations = Reservation.objects.filter(status='pending').count()
    
    # Membership stats
    membership_tiers_count = MembershipTier.objects.count()
    applications_count = MembershipApplication.objects.count()
    pending_applications = MembershipApplication.objects.filter(status='pending').count()
    
    # Donation stats
    donations_count = CharityDonation.objects.count()
    total_donations = CharityDonation.objects.filter(status='verified').aggregate(total=Sum('amount'))['total'] or 0
    
    # Payment methods stats
    payment_methods_count = PaymentMethod.objects.count()
    crypto_wallets_count = CryptoWallet.objects.count()
    
    context = {
        'celebrities_count': celebrities_count,
        'reservations_count': reservations_count,
        'pending_reservations': pending_reservations,
        'membership_tiers_count': membership_tiers_count,
        'applications_count': applications_count,
        'pending_applications': pending_applications,
        'donations_count': donations_count,
        'total_donations': total_donations,
        'payment_methods_count': payment_methods_count,
        'crypto_wallets_count': crypto_wallets_count,
    }
    
    return render(request, 'admin_panel/dashboard.html', context)

# Celebrity views (existing)
@login_required
def celebrity_list(request):
    celebrities = Celebrity.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/celebrity_list.html', {'celebrities': celebrities})

@login_required
def add_celebrity(request):
    if request.method == 'POST':
        form = CelebrityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Celebrity added successfully!')
            return redirect('admin_celebrity_list')
    else:
        form = CelebrityForm()
    
    return render(request, 'admin_panel/celebrity_form.html', {'form': form, 'action': 'Add'})

@login_required
def edit_celebrity(request, celebrity_id):
    celebrity = get_object_or_404(Celebrity, id=celebrity_id)
    
    if request.method == 'POST':
        form = CelebrityForm(request.POST, request.FILES, instance=celebrity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Celebrity updated successfully!')
            return redirect('admin_celebrity_list')
    else:
        form = CelebrityForm(instance=celebrity)
    
    return render(request, 'admin_panel/celebrity_form.html', {'form': form, 'action': 'Edit', 'celebrity': celebrity})

@login_required
def delete_celebrity(request, celebrity_id):
    celebrity = get_object_or_404(Celebrity, id=celebrity_id)
    
    if request.method == 'POST':
        celebrity.delete()
        messages.success(request, 'Celebrity deleted successfully!')
        return redirect('admin_celebrity_list')
    
    return render(request, 'admin_panel/delete_confirmation.html', {'celebrity': celebrity})

# Reservation views (existing)
@login_required
def reservation_list(request):
    reservations = Reservation.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/reservation_list.html', {'reservations': reservations})

@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'admin_panel/reservation_detail.html', {'reservation': reservation})

@login_required
def update_reservation_status(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [choice[0] for choice in Reservation.STATUS_CHOICES]:
            reservation.status = new_status
            reservation.save()
            
            # Send status update email to user
            subject = f'Update on your booking with {reservation.celebrity.name}'
            html_message = render_to_string('admin_panel/emails/status_update.html', {
                'reservation': reservation,
                'celebrity': reservation.celebrity,
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [reservation.user_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, f'Reservation status updated to {new_status}')
        
        return redirect('admin_reservation_detail', reservation_id=reservation.id)
    
    return redirect('admin_reservation_list')

# Payment Method views (new)
@login_required
def payment_method_list(request):
    payment_methods = PaymentMethod.objects.all()
    return render(request, 'admin_panel/payment_method_list.html', {'payment_methods': payment_methods})

@login_required
def add_payment_method(request):
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment method added successfully!')
            return redirect('admin_payment_method_list')
    else:
        form = PaymentMethodForm()
    
    return render(request, 'admin_panel/payment_method_form.html', {'form': form, 'action': 'Add'})

@login_required
def edit_payment_method(request, payment_method_id):
    payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)
    
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, instance=payment_method)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment method updated successfully!')
            return redirect('admin_payment_method_list')
    else:
        form = PaymentMethodForm(instance=payment_method)
    
    return render(request, 'admin_panel/payment_method_form.html', {
        'form': form, 
        'action': 'Edit', 
        'payment_method': payment_method
    })

@login_required
def delete_payment_method(request, payment_method_id):
    payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)
    
    if request.method == 'POST':
        payment_method.delete()
        messages.success(request, 'Payment method deleted successfully!')
        return redirect('admin_payment_method_list')
    
    return render(request, 'admin_panel/delete_confirmation.html', {'payment_method': payment_method})

# Crypto Wallet views (new)
@login_required
def crypto_wallet_list(request):
    crypto_wallets = CryptoWallet.objects.all()
    return render(request, 'admin_panel/crypto_wallet_list.html', {'crypto_wallets': crypto_wallets})

@login_required
def add_crypto_wallet(request):
    if request.method == 'POST':
        form = CryptoWalletForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crypto wallet added successfully!')
            return redirect('admin_crypto_wallet_list')
    else:
        form = CryptoWalletForm()
    
    return render(request, 'admin_panel/crypto_wallet_form.html', {'form': form, 'action': 'Add'})

@login_required
def edit_crypto_wallet(request, wallet_id):
    wallet = get_object_or_404(CryptoWallet, id=wallet_id)
    
    if request.method == 'POST':
        form = CryptoWalletForm(request.POST, request.FILES, instance=wallet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crypto wallet updated successfully!')
            return redirect('admin_crypto_wallet_list')
    else:
        form = CryptoWalletForm(instance=wallet)
    
    return render(request, 'admin_panel/crypto_wallet_form.html', {
        'form': form, 
        'action': 'Edit', 
        'wallet': wallet
    })

@login_required
def delete_crypto_wallet(request, wallet_id):
    wallet = get_object_or_404(CryptoWallet, id=wallet_id)
    
    if request.method == 'POST':
        wallet.delete()
        messages.success(request, 'Crypto wallet deleted successfully!')
        return redirect('admin_crypto_wallet_list')
    
    return render(request, 'admin_panel/delete_confirmation.html', {'wallet': wallet})

# Membership Tier views (new)
@login_required
def membership_tier_list(request):
    tiers = MembershipTier.objects.all()
    return render(request, 'admin_panel/membership_tier_list.html', {'tiers': tiers})

@login_required
def add_membership_tier(request):
    if request.method == 'POST':
        form = MembershipTierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membership tier added successfully!')
            return redirect('admin_membership_tier_list')
    else:
        form = MembershipTierForm()
    
    return render(request, 'admin_panel/membership_tier_form.html', {'form': form, 'action': 'Add'})

@login_required
def edit_membership_tier(request, tier_id):
    tier = get_object_or_404(MembershipTier, id=tier_id)
    
    if request.method == 'POST':
        form = MembershipTierForm(request.POST, instance=tier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membership tier updated successfully!')
            return redirect('admin_membership_tier_list')
    else:
        form = MembershipTierForm(instance=tier)
    
    return render(request, 'admin_panel/membership_tier_form.html', {
        'form': form, 
        'action': 'Edit', 
        'tier': tier
    })

@login_required
def delete_membership_tier(request, tier_id):
    tier = get_object_or_404(MembershipTier, id=tier_id)
    
    if request.method == 'POST':
        tier.delete()
        messages.success(request, 'Membership tier deleted successfully!')
        return redirect('admin_membership_tier_list')
    
    return render(request, 'admin_panel/delete_confirmation.html', {'tier': tier})

# Membership Application views (new)
@login_required
def membership_application_list(request):
    applications = MembershipApplication.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/membership_application_list.html', {'applications': applications})

@login_required
def membership_application_detail(request, application_id):
    application = get_object_or_404(MembershipApplication, id=application_id)
    return render(request, 'admin_panel/membership_application_detail.html', {'application': application})

@login_required
def update_membership_application_status(request, application_id):
    application = get_object_or_404(MembershipApplication, id=application_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [choice[0] for choice in MembershipApplication.STATUS_CHOICES]:
            application.status = new_status
            application.save()
            
            # Send status update email to user
            subject = f'Update on your Membership Application'
            html_message = render_to_string('admin_panel/emails/membership_status_update.html', {
                'application': application,
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [application.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, f'Membership application status updated to {new_status}')
        
        return redirect('admin_membership_application_detail', application_id=application.id)
    
    return redirect('admin_membership_application_list')

# Charity Donation views (new)
@login_required
def charity_donation_list(request):
    donations = CharityDonation.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/charity_donation_list.html', {'donations': donations})

@login_required
def charity_donation_detail(request, donation_id):
    donation = get_object_or_404(CharityDonation, id=donation_id)
    return render(request, 'admin_panel/charity_donation_detail.html', {'donation': donation})

@login_required
def update_charity_donation_status(request, donation_id):
    donation = get_object_or_404(CharityDonation, id=donation_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [choice[0] for choice in CharityDonation.STATUS_CHOICES]:
            donation.status = new_status
            donation.save()
            
            # Send status update email to user
            subject = f'Update on your Donation'
            html_message = render_to_string('admin_panel/emails/donation_status_update.html', {
                'donation': donation,
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [donation.donor_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, f'Donation status updated to {new_status}')
        
        return redirect('admin_charity_donation_detail', donation_id=donation.id)
    
    return redirect('admin_charity_donation_list')

# Email functionality (existing)
@login_required
def send_email(request, reservation_id=None):
    reservation = None
    initial_data = {}
    
    if reservation_id:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        initial_data = {
            'recipient_email': reservation.user_email,
            'subject': f'Regarding your booking with {reservation.celebrity.name}',
        }
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            html_message = render_to_string('admin_panel/emails/custom_email.html', {
                'message': message,
                'reservation': reservation,
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, f'Email sent to {recipient_email} successfully!')
            
            if reservation:
                return redirect('admin_reservation_detail', reservation_id=reservation.id)
            return redirect('admin_dashboard')
    else:
        form = EmailForm(initial=initial_data)
    
    context = {
        'form': form,
        'reservation': reservation,
    }
    
    return render(request, 'admin_panel/send_email.html', context)

@login_required
def send_email_to_applicant(request, application_id=None):
    application = None
    initial_data = {}
    
    if application_id:
        application = get_object_or_404(MembershipApplication, id=application_id)
        initial_data = {
            'recipient_email': application.email,
            'subject': f'Regarding your Membership Application',
        }
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            html_message = render_to_string('admin_panel/emails/custom_email.html', {
                'message': message,
                'application': application,
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, f'Email sent to {recipient_email} successfully!')
            
            if application:
                return redirect('admin_membership_application_detail', application_id=application.id)
            return redirect('admin_dashboard')
    else:
        form = EmailForm(initial=initial_data)
    
    context = {
        'form': form,
        'application': application,
    }
    
    return render(request, 'admin_panel/send_email.html', context)

@login_required
def send_email_to_donor(request, donation_id=None):
    donation = None
    initial_data = {}
    
    if donation_id:
        donation = get_object_or_404(CharityDonation, id=donation_id)
        initial_data = {
            'recipient_email': donation.donor_email,
            'subject': f'Regarding your Donation',
        }
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            html_message = render_to_string('admin_panel/emails/custom_email.html', {
                'message': message,
                'donation': donation,
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, f'Email sent to {recipient_email} successfully!')
            
            if donation:
                return redirect('admin_charity_donation_detail', donation_id=donation.id)
            return redirect('admin_dashboard')
    else:
        form = EmailForm(initial=initial_data)
    
    context = {
        'form': form,
        'donation': donation,
    }
    
    return render(request, 'admin_panel/send_email.html', context)