from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, help_text="Height in cm"
    )
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight in kg"
    )
    activity_level = models.CharField(
        max_length=20,
        choices=[
            ("sedentary", "Sedentary"),
            ("lightly_active", "Lightly Active"),
            ("moderately_active", "Moderately Active"),
            ("very_active", "Very Active"),
            ("extra_active", "Extra Active"),
        ],
        default="moderately_active",
    )
    dietary_goals = models.JSONField(
        default=dict,
        blank=True,
        help_text="Goals like {'calories': 2000, 'protein': 150}",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    

class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
