from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

def upload_path( instance,filname):
    return '/'.join(['covers',filname])

class Price_cut(models.Model):
    cut=models.IntegerField()

class Price(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    amount = models.IntegerField()
    joined_by = models.ForeignKey(User , on_delete=models.SET_NULL ,null=True ,related_name='user_joined')
    request_to_join=models.BooleanField(default=False)
    accetp_to_play = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    joined_time = models.DateTimeField(null=True, blank=True)
    result_updated= models.BooleanField(default=False)
    closed=models.BooleanField(default=False)
    user_payment=models.BooleanField(default=False)
    joined_user_payment=models.BooleanField(default=False)



class Room(models.Model):
    room_id = models.OneToOneField(Price , on_delete=models.CASCADE)
    room_code = models.IntegerField(null=True)
   


class result_win(models.Model):
    result_id = models.ForeignKey(Price , on_delete=models.CASCADE)
    img =models.ImageField(upload_to=upload_path,  null=True , blank=True )
    won = models.ForeignKey(User , on_delete=models.CASCADE)

class result_loss(models.Model):
    result_id = models.ForeignKey(Price , on_delete=models.CASCADE)
    lost= models.ForeignKey(User , on_delete=models.CASCADE)

class result_cancel(models.Model):
    result_id = models.ForeignKey(Price , on_delete=models.CASCADE)
    cancel = models.ForeignKey(User , on_delete=models.CASCADE)


class match_withdrawl_payment(models.Model):
    price_model = models.ForeignKey(Price , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    amount= models.IntegerField()
    date_time = models.DateTimeField(auto_now=True)

class match_deposit_payment(models.Model):
    price_model = models.ForeignKey(Price , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    amount= models.IntegerField()
    date_time = models.DateTimeField(auto_now=True)
