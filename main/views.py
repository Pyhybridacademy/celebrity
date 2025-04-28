from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings
from .models import (
    Celebrity, Reservation, PaymentMethod, CryptoWallet, 
    MembershipTier, MembershipApplication, CharityDonation
)
from .forms import ReservationForm, MembershipApplicationForm, CharityDonationForm

def home(request):
    celebrities = Celebrity.objects.filter(available=True)
    return render(request, 'main/home.html', {'celebrities': celebrities})

def celebrity_list(request):
    celebrities = Celebrity.objects.filter(available=True)
    return render(request, 'main/celebrity_list.html', {'celebrities': celebrities})

def celebrity_detail(request, celebrity_id):
    celebrity = get_object_or_404(Celebrity, id=celebrity_id)
    return render(request, 'main/celebrity_detail.html', {'celebrity': celebrity})

def book_reservation(request, celebrity_id):
    celebrity = get_object_or_404(Celebrity, id=celebrity_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.celebrity = celebrity
            reservation.save()
            
            # Send confirmation email to user
            subject = f'Booking Confirmation for {celebrity.name}'
            html_message = render_to_string('main/emails/booking_confirmation.html', {
                'reservation': reservation,
                'celebrity': celebrity,
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = reservation.user_email
            
            send_mail(
                subject,
                plain_message,
                from_email,
                [to_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Send notification to admin
            admin_subject = f'New Booking: {reservation.user_name} with {celebrity.name}'
            admin_html_message = render_to_string('main/emails/admin_notification.html', {
                'reservation': reservation,
                'celebrity': celebrity,
            })
            admin_plain_message = strip_tags(admin_html_message)
            
            send_mail(
                admin_subject,
                admin_plain_message,
                from_email,
                [settings.DEFAULT_FROM_EMAIL],  # Send to admin email
                html_message=admin_html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Your booking has been submitted successfully! Check your email for confirmation.')
            return redirect('booking_confirmation', reservation_id=reservation.id)
    else:
        form = ReservationForm()
    
    return render(request, 'main/book_reservation.html', {
        'form': form,
        'celebrity': celebrity,
    })

def booking_confirmation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'main/booking_confirmation.html', {'reservation': reservation})

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

# New views for membership and donation features

def membership_info(request):
    tiers = MembershipTier.objects.all()
    return render(request, 'main/membership_info.html', {'tiers': tiers})

def apply_membership(request):
    crypto_wallets = CryptoWallet.objects.filter(is_active=True)
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = MembershipApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            
            # Send confirmation email to user
            subject = 'Fan Membership Application Received'
            html_message = render_to_string('main/emails/membership_confirmation.html', {
                'application': application,
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = application.email
            
            send_mail(
                subject,
                plain_message,
                from_email,
                [to_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Send notification to admin
            admin_subject = f'New Membership Application: {application.full_name}'
            admin_html_message = render_to_string('main/emails/admin_membership_notification.html', {
                'application': application,
            })
            admin_plain_message = strip_tags(admin_html_message)
            
            send_mail(
                admin_subject,
                admin_plain_message,
                from_email,
                [settings.DEFAULT_FROM_EMAIL],  # Send to admin email
                html_message=admin_html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Your membership application has been submitted successfully! Check your email for confirmation.')
            return redirect('membership_confirmation', application_id=application.id)
    else:
        form = MembershipApplicationForm()
    
    return render(request, 'main/apply_membership.html', {
        'form': form,
        'crypto_wallets': crypto_wallets,
        'payment_methods': payment_methods,
    })

def membership_confirmation(request, application_id):
    application = get_object_or_404(MembershipApplication, id=application_id)
    return render(request, 'main/membership_confirmation.html', {'application': application})

def donate_charity(request):
    crypto_wallets = CryptoWallet.objects.filter(is_active=True)
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = CharityDonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save()
            
            # Send confirmation email to user
            subject = 'Thank You for Your Donation'
            html_message = render_to_string('main/emails/donation_confirmation.html', {
                'donation': donation,
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = donation.donor_email
            
            send_mail(
                subject,
                plain_message,
                from_email,
                [to_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Send notification to admin
            admin_subject = f'New Charity Donation: ${donation.amount} from {donation.donor_name}'
            admin_html_message = render_to_string('main/emails/admin_donation_notification.html', {
                'donation': donation,
            })
            admin_plain_message = strip_tags(admin_html_message)
            
            send_mail(
                admin_subject,
                admin_plain_message,
                from_email,
                [settings.DEFAULT_FROM_EMAIL],  # Send to admin email
                html_message=admin_html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Your donation has been submitted successfully! Check your email for confirmation.')
            return redirect('donation_confirmation', donation_id=donation.id)
    else:
        form = CharityDonationForm()
    
    return render(request, 'main/donate_charity.html', {
        'form': form,
        'crypto_wallets': crypto_wallets,
        'payment_methods': payment_methods,
    })

def donation_confirmation(request, donation_id):
    donation = get_object_or_404(CharityDonation, id=donation_id)
    return render(request, 'main/donation_confirmation.html', {'donation': donation})

def donation_list(request):
    donations = CharityDonation.objects.filter(status='verified', anonymous=False).order_by('-created_at')
    total_amount = CharityDonation.objects.filter(status='verified').aggregate(models.Sum('amount'))['amount__sum'] or 0
    return render(request, 'main/donation_list.html', {
        'donations': donations,
        'total_amount': total_amount
    })
