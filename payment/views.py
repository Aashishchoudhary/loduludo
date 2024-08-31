from django.shortcuts import render ,redirect
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from .models import Payment_deposit ,Payment_withdrwable
from .serializer import Payment_deposit_serializer , Payment_withdrawable_serializer


def wallet(request):
    balance= get_deposit_balance(request.user.id)+get_withdrawable_balance(request.user.id)
    print(balance)
    return render(request ,'wallet.html',{'bal':balance})


class payment_deposit_view(APIView):
    def get(self , request):
        user = request.user
        bal = Payment_deposit.objects.filter(user =user.id)
        bal_serliazer = Payment_deposit_serializer(bal , many=True).data
        return Response(bal_serliazer)
    

    def post(self, request):
        user = request.user
        data={
            'user':user.id,
            'deposit_balance':200
        }
        ser= Payment_deposit_serializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data , status=200)
        return Response(ser.errors , status=400)
    
    def patch(self , request):
        user= request.user
        bal=Payment_deposit.objects.get(user=user.id)
        ser= Payment_deposit_serializer(bal).data['deposit_balance']
        data ={
            "deposit_balance":200+ser
            }
        ser_save= Payment_deposit_serializer(bal , data=data , partial=True)
        if ser_save.is_valid():
            ser_save.save()
            return Response(ser_save.data , status=200)
        
        return Response(ser_save.errors , status=200)
    
class payment_withdrawable_view(APIView):
    def get(self , request):
        user = request.user
        bal = Payment_withdrwable.objects.filter(user =user.id)
        bal_serliazer = Payment_withdrawable_serializer(bal , many=True).data
        return Response(bal_serliazer)
    

    def post(self, request):
        user = request.user
        data={
            'user':user.id,
            'withdraable_balance':200
        }
        ser=  Payment_withdrawable_serializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data , status=200)
        return Response(ser.errors , status=400)
    
    def patch(self , request):
        user= request.user
        bal=Payment_withdrwable.objects.get(user=user.id)
        ser=  Payment_withdrawable_serializer(bal).data['withdraable_balance']
        data ={
            "withdraable_balance":200+ser
            }
        ser_save=  Payment_withdrawable_serializer(bal , data=data , partial=True)
        if ser_save.is_valid():
            ser_save.save()
            return Response(ser_save.data , status=200)
        
        return Response(ser_save.errors , status=200)
        


def get_deposit_balance(user):
    bal = Payment_deposit.objects.filter(user=user)
    bal_serliazer = Payment_deposit_serializer(bal , many=True).data
    return bal_serliazer[0]['deposit_balance']


def patch_deposit_balance(user,amount):

    bal=Payment_deposit.objects.get(user=user)
    ser=  Payment_deposit_serializer(bal).data['deposit_balance']
    data ={
        "deposit_balance":amount+ser
        }
    ser_save=  Payment_deposit_serializer(bal , data=data , partial=True)
    if ser_save.is_valid():
        ser_save.save()
        return Response(ser_save.data , status=200)
    
    return Response(ser_save.errors , status=200)

def get_withdrawable_balance(user):
    bal = Payment_withdrwable.objects.filter(user =user)
    bal_serliazer = Payment_withdrawable_serializer(bal , many=True).data
    return bal_serliazer[0]['withdraable_balance']


def patch_withdrawble_balance(user , amount):
    
    bal=Payment_withdrwable.objects.get(user=user)
    ser=  Payment_withdrawable_serializer(bal).data['withdraable_balance']

    data ={
        "withdraable_balance":ser+amount
        }
    ser_save=  Payment_withdrawable_serializer(bal , data=data , partial=True)
    if ser_save.is_valid():
        ser_save.save()
        return Response(ser_save.data , status=200)
    
    return Response(ser_save.errors , status=200)
