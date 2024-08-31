from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()

from django.db.models.signals import post_save
from django.dispatch import receiver

class Payment_deposit(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    deposit_balance = models.IntegerField(null=True , blank=True)

class Payment_withdrwable(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    withdraable_balance = models.IntegerField(null=True , blank=True)




@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        Payment_deposit.objects.create(user=instance ,deposit_balance=0)
        Payment_withdrwable.objects.create(user=instance ,withdraable_balance=0)