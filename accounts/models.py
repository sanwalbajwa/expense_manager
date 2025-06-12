from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'United States Dollar ($)'),
        ('PKR', 'Pakistani Rupee (₨)'),
        ('GBP', 'British Pound (£)'),
        ('INR', 'Indian Rupee (₹)'),
        ('SAR', 'Saudi Riyal (﷼)'),
        ('AED', 'UAE Dirham (د.إ)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    preferred_currency = models.CharField(
        max_length=3, 
        choices=CURRENCY_CHOICES, 
        default='USD'
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a profile when a new user is created
        UserProfile.objects.create(user=instance)
    else:
        # For existing users, try to save the profile or create if it doesn't exist
        try:
            instance.profile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)