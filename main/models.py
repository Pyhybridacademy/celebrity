# main/models.py
from django.db import models
from django.utils import timezone

class Celebrity(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='celebrities/')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Celebrities"

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE, related_name='reservations')
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    duration_hours = models.PositiveIntegerField(default=1)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_name} - {self.celebrity.name} - {self.booking_date}"
    
    @property
    def total_cost(self):
        return self.celebrity.hourly_rate * self.duration_hours