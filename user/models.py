from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser ,BaseUserManager
# Create your models here.


class CustomUserManager(BaseUserManager ,):
    def create_user(self,username , password ,email=None):
        if not username:
            raise ValueError("User must enter phone number")
        
        user=self.model(username=username)
        user.set_password(password)
        user.is_staff=False
        user.is_admin=False
        user.is_active=True
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username , password ,email=None):
        user=self.create_user(username , password=password)
        user.is_staff=True
        user.is_admin=True
        user.is_active=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
    

class CustomUser(AbstractUser):
   
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$')

    username=models.CharField(validators=[phone_regex] , max_length=13 , unique=True)
    standard=models.CharField(max_length=3 , blank=True , null=True)
    first_login=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff       = models.BooleanField(default=False)
    is_admin       = models.BooleanField(default=False)

    timestamp   = models.DateTimeField(auto_now_add=True)

    objects=CustomUserManager()
    USERNAME_FIELD='username'
    # REQUIRED_FIELDS = []

    def __str__(self):
        return self.username



