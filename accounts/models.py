from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.utils import timezone
# Create your models here.
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            return ValueError('You must provide an email address')
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True :
            return ValueError('super user must be is_staff True')
        if extra_fields.get('is_superuser') is not True:
            return ValueError("must be superuser")
        return self.create_user(email, password, **extra_fields)
        
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length= 20,  null = False)
    first_name = models.CharField(max_length = 20, null = False, db_index = True)
    last_name = models.CharField(max_length = 20, null = False, db_index = True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    is_logged_in = models.BooleanField(default=False)
    # otp = models.CharField(max_length=6, blank=True, null=True)  # Field to store OTP

    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default = timezone.now())
    
