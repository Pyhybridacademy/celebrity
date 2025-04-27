# admin_panel/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings
from main.models import Celebrity, Reservation
from .forms import CelebrityForm, EmailForm

@login_required
def admin_dashboard(request):
    celebrities_count = Celebrity.objects.count()
    reservations_count = Reservation.objects.count()
    pending_reservations = Reservation.objects.filter(status='pending').count()
    
    context = {
        'celebrities_count': celebrities_count,
        'reservations_count': reservations_count,
        'pending_reservations': pending_reservations,
    }
    
    return render(request, 'admin_panel/dashboard.html', context)

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