from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_tomtom = models.CharField(max_length=255, null=True, blank=True)
    
    @receiver(post_save, sender=User) #add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User) #add this
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


    def __str__(self):
        return f'{self.user.username} Profile'