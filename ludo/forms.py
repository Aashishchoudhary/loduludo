from django import forms
from .models import Price ,Room ,result_win , result_cancel , result_loss


class SetAmountForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Price
        fields = ['amount']
        # exclude = ['user' ,'joined_by' ,'']



class Room_win_Form(forms.ModelForm):
    class Meta:
        model = result_win
        fields ='__all__'
        exclude = ['result_id']

class Room_loss_Form(forms.ModelForm):
    class Meta:
        model = result_loss
        fields ='__all__'
        exclude=['reult_id']

class Room_cancel_Form(forms.ModelForm):
    class Meta:
        model = result_cancel
        fields ='__all__'
        exclude=['reult_id']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields ='__all__'
        exclude = ['room_id']