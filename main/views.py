# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings
from .models import Celebrity, Reservation
from .forms import ReservationForm

def home(request):
    celebrities = Celebrity.objects.filter(available=True)
    return render(request, 'main/home.html', {'celebrities': celebrities})

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