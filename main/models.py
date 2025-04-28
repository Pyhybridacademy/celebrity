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

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class CryptoWallet(models.Model):
    currency = models.CharField(max_length=50)
    wallet_address = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='crypto_wallets/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.currency} Wallet"

class MembershipTier(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=365)
    description = models.TextField()
    benefits = models.TextField()
    
    def __str__(self):
        return self.name

class MembershipApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('crypto', 'Cryptocurrency'),
        ('giftcard', 'Gift Card'),
    )
    
    tier = models.ForeignKey(MembershipTier, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_proof = models.ImageField(upload_to='payment_proofs/')
    payment_details = models.TextField(help_text="Transaction ID or gift card details")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.tier.name} Membership"

class CharityDonation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('crypto', 'Cryptocurrency'),
        ('giftcard', 'Gift Card'),
    )
    
    donor_name = models.CharField(max_length=100)
    donor_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_proof = models.ImageField(upload_to='donation_proofs/')
    payment_details = models.TextField(help_text="Transaction ID or gift card details")
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.donor_name} - ${self.amount}"
