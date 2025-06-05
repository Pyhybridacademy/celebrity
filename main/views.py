from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings
from .models import (
    Celebrity, Reservation, PaymentMethod, CryptoWallet, 
    MembershipTier, MembershipApplication, CharityDonation,
    ModelingContract, BrandAmbassador, SiteSettings, ContactMessage
)
from .forms import (
    ReservationForm, MembershipApplicationForm, CharityDonationForm,
    ModelingContractForm, BrandAmbassadorForm, ContactMessageForm
)

def home(request):
    celebrities = Celebrity.objects.filter(available=True)
    site_settings = SiteSettings.objects.first()  # Get the first (and only) settings instance
    return render(request, 'main/home.html', {'celebrities': celebrities, 'site_settings': site_settings})

def celebrity_list(request):
    celebrities = Celebrity.objects.filter(available=True)
    site_settings = SiteSettings.objects.first()
    return render(request, 'main/celebrity_list.html', {'celebrities': celebrities, 'site_settings': site_settings})

def celebrity_detail(request, celebrity_id):
    celebrity = get_object_or_404(Celebrity, id=celebrity_id)
    other_celebrities = Celebrity.objects.filter(available=True).exclude(id=celebrity.id).order_by('?')[:4]  # Random 4 other celebrities
    return render(request, 'main/celebrity_detail.html', {
        'celebrity': celebrity,
        'other_celebrities': other_celebrities,
    })

def book_reservation(request, celebrity_id):
    celebrity = get_object_or_404(Celebrity, id=celebrity_id)
    site_settings = SiteSettings.objects.first()
    
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
                'site_settings': site_settings,
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
                'site_settings': site_settings,
            })
            admin_plain_message = strip_tags(admin_html_message)
            
            send_mail(
                admin_subject,
                admin_plain_message,
                from_email,
                [settings.DEFAULT_FROM_EMAIL],
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
        'site_settings': site_settings,
    })

def booking_confirmation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    site_settings = SiteSettings.objects.first()
    return render(request, 'main/booking_confirmation.html', {'reservation': reservation, 'site_settings': site_settings})

def about(request):
    site_settings = SiteSettings.objects.first()
    return render(request, 'main/about.html', {'site_settings': site_settings})

def contact(request):
    site_settings = SiteSettings.objects.first()
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send confirmation email to user
            subject = 'Thank You for Contacting Us'
            html_message = render_to_string('main/emails/contact_confirmation.html', {
                'contact_message': contact_message,
                'site_settings': site_settings,
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = contact_message.email
            
            send_mail(
                subject,
                plain_message,
                from_email,
                [to_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Send notification to admin
            admin_subject = f'New Contact Message: {contact_message.subject}'
            admin_html_message = render_to_string('main/emails/admin_contact_notification.html', {
                'contact_message': contact_message,
                'site_settings': site_settings,
            })
            admin_plain_message = strip_tags(admin_html_message)
            
            send_mail(
                admin_subject,
                admin_plain_message,
                from_email,
                [settings.DEFAULT_FROM_EMAIL],
                html_message=admin_html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully! Check your email for confirmation.')
            return redirect('contact')
    else:
        form = ContactMessageForm()
    
    return render(request, 'main/contact.html', {
        'form': form,
        'site_settings': site_settings,
    })

def membership_info(request):
    tiers = MembershipTier.objects.all()
    site_settings = SiteSettings.objects.first()
    return render(request, 'main/membership_info.html', {'tiers': tiers, 'site_settings': site_settings})

def apply_membership(request):
    crypto_wallets = CryptoWallet.objects.filter(is_active=True)
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    site_settings = SiteSettings.objects.first()
    
    if request.method == 'POST':
        form = MembershipApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            
            # Send confirmation email to user
            subject = 'Fan Membership Application Received'
            html_message = render_to_string('main/emails/membership_confirmation.html', {
                'application': application,
                'site_settings': site_settings,
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
                'site_settings': site_settings,
            })
            admin_plain_message = strip_tags(admin_html_message)
            
            send_mail(
                admin_subject,
                admin_plain_message,
                from_email,
                [settings.DEFAULT_FROM_EMAIL],
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
        'site_settings': site_settings,
    })

def membership_confirmation(request, application_id):
    application = get_object_or_404(MembershipApplication, id=application_id)
    site_settings = SiteSettings.objects.first()
    return render(request, 'main/membership_confirmation.html', {'application': application, 'site_settings': site_settings})

def donate_charity(request):
    crypto_wallets = CryptoWallet.objects.filter(is_active=True)
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    site_settings = SiteSettings.objects.first()
    
    if request.method == 'POST':
        form = CharityDonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save()
            
            # Send confirmation email to user
            subject = 'Thank You for Your Donation'
            html_message = render_to_string('main/emails/donation_confirmation.html', {
                'donation': donation,
                'site_settings': site_settings,
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
                'site_settings': site_settings,
            })
            admin_plain_message = strip_tags(admin_html_message)
            
            send_mail(
                admin_subject,
                admin_plain_message,
                from_email,
                [settings.DEFAULT_FROM_EMAIL],
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
        'site_settings': site_settings,
    })

def donation_confirmation(request, donation_id):
    donation = get_object_or_404(CharityDonation, id=donation_id)
    site_settings = SiteSettings.objects.first()
    return render(request, 'main/donation_confirmation.html', {'donation': donation, 'site_settings': site_settings})

def donation_list(request):
    donations = CharityDonation.objects.filter(status='verified', anonymous=False).order_by('-created_at')
    total_amount = CharityDonation.objects.filter(status='verified').aggregate(models.Sum('amount'))['amount__sum'] or 0
    site_settings = SiteSettings.objects.first()
    return render(request, 'main/donation_list.html', {
        'donations': donations,
        'total_amount': total_amount,
        'site_settings': site_settings,
    })

def apply_modeling_contract(request):
    crypto_wallets = CryptoWallet.objects.filter(is_active=True)
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    site_settings = SiteSettings.objects.first()
    
    if request.method == 'POST':
        form = ModelingContractForm(request.POST, request.FILES)
        if form.is_valid():
            contract = form.save()
            
            # Send confirmation email to user
            subject = 'Modeling Contract Application Received'
            html_message = render_to_string('main/emails/modeling_contract_confirmation.html', {
                'contract': contract,
                'site_settings': site_settings,
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = contract.email
            
            send_mail(
                subject,
                plain_message,
                from_email,
                [to_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Send notification to admin
            admin_subject = f'New Modeling Contract Application: {contract.full_name}'
            admin_html_message = render_to_string('main/emails/admin_modeling_contract_notification.html', {
                'contract': contract,
                'site_settings': site_settings,
            })
            admin_plain_message = strip_tags(admin_html_message)
            
            send_mail(
                admin_subject,
                admin_plain_message,
                from_email,
                [settings.DEFAULT_FROM_EMAIL],
                html_message=admin_html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Your modeling contract application has been submitted successfully! Check your email for confirmation.')
            return redirect('modeling_contract_confirmation', contract_id=contract.id)
    else:
        form = ModelingContractForm()
    
    return render(request, 'main/apply_modeling_contract.html', {
        'form': form,
        'crypto_wallets': crypto_wallets,
        'payment_methods': payment_methods,
        'site_settings': site_settings,
    })

def modeling_contract_confirmation(request, contract_id):
    contract = get_object_or_404(ModelingContract, id=contract_id)
    site_settings = SiteSettings.objects.first()
    return render(request, 'main/modeling_contract_confirmation.html', {'contract': contract, 'site_settings': site_settings})

def apply_brand_ambassador(request):
    crypto_wallets = CryptoWallet.objects.filter(is_active=True)
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    site_settings = SiteSettings.objects.first()
    
    if request.method == 'POST':
        form = BrandAmbassadorForm(request.POST, request.FILES)
        if form.is_valid():
            ambassador = form.save()
            
            # Send confirmation email to user
            subject = 'Brand Ambassador Application Received'
            html_message = render_to_string('main/emails/brand_ambassador_confirmation.html', {
                'ambassador': ambassador,
                'site_settings': site_settings,
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = ambassador.email
            
            send_mail(
                subject,
                plain_message,
                from_email,
                [to_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Send notification to admin
            admin_subject = f'New Brand Ambassador Application: {ambassador.full_name}'
            admin_html_message = render_to_string('main/emails/admin_brand_ambassador_notification.html', {
                'ambassador': ambassador,
                'site_settings': site_settings,
            })
            admin_plain_message = strip_tags(admin_html_message)
            
            send_mail(
                admin_subject,
                admin_plain_message,
                from_email,
                [settings.DEFAULT_FROM_EMAIL],
                html_message=admin_html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Your brand ambassador application has been submitted successfully! Check your email for confirmation.')
            return redirect('brand_ambassador_confirmation', ambassador_id=ambassador.id)
    else:
        form = BrandAmbassadorForm()
    
    return render(request, 'main/apply_brand_ambassador.html', {
        'form': form,
        'crypto_wallets': crypto_wallets,
        'payment_methods': payment_methods,
        'site_settings': site_settings,
    })

def brand_ambassador_confirmation(request, ambassador_id):
    ambassador = get_object_or_404(BrandAmbassador, id=ambassador_id)
    site_settings = SiteSettings.objects.first()
    return render(request, 'main/brand_ambassador_confirmation.html', {'ambassador': ambassador, 'site_settings': site_settings})