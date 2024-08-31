from django.urls import path
from . import views

urlpatterns = [ 
path('wallet/' , views.wallet , name = 'wallet'),
path('deposit-balcance/' , views.payment_deposit_view.as_view())

]