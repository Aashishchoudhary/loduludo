from rest_framework import serializers

from .models import Payment_deposit , Payment_withdrwable

class Payment_deposit_serializer(serializers.ModelSerializer):
    class Meta:
        model=Payment_deposit
        fields='__all__'
class Payment_withdrawable_serializer(serializers.ModelSerializer):
    class Meta:
        model=Payment_withdrwable
        fields='__all__'