from rest_framework import serializers
from .models import Price , Room  ,Price_cut  ,result_cancel , result_win , result_loss ,match_deposit_payment , match_withdrawl_payment
from django.contrib.auth import get_user_model
User = get_user_model()


class PriceSerializier(serializers.ModelSerializer):
    class Meta:
        model=Price
        fields='__all__'
        
class RoomSerializier(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields='__all__'


class PrcieCutSerializer(serializers.ModelSerializer):
    class Meta:
        model=Price_cut
        fields="__all__"

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"

class Resut_Win_Serializer(serializers.ModelSerializer):
    class Meta:
        model=result_win
        fields="__all__"


class Resut_Loss_Serializer(serializers.ModelSerializer):
    class Meta:
        model=result_loss
        fields="__all__"

class Result_cancel_Serializer(serializers.ModelSerializer):
    class Meta:
        model=result_cancel
        fields="__all__"

class Match_deposit_payment_serializer(serializers.ModelSerializer):
    class Meta:
        model= match_deposit_payment
        fields="__all__"

class Match_withdrawal_payment_serializer(serializers.ModelSerializer):
    class Meta:
        model= match_withdrawl_payment
        fields="__all__"