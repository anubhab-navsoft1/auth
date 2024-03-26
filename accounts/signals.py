from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CustomUser


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    # User = get_user_model
    
    CustomUser.objects.filter(pk = user.pk).update(is_logged_in=True)
    
@receiver(user_logged_out) 
def user_logged_out_handler(sender, request, user, **kwargs):
    # User = get_user_model()
    
    CustomUser.objects.filter(pk=user.pk).update(is_logged_in=False)