from payment.views import get_deposit_balance, get_withdrawable_balance, patch_deposit_balance, patch_withdrawble_balance
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permission import check_is_staff
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import SetAmountForm, RoomForm
# Create your views here.
from django.contrib.auth import get_user_model
from .models import Room, Price, result_win, result_cancel, result_loss, match_withdrawl_payment, match_deposit_payment
from .serializers import RoomSerializier, PriceSerializier, UserSerializer, Resut_Win_Serializer, Resut_Loss_Serializer, Result_cancel_Serializer, Match_deposit_payment_serializer, Match_withdrawal_payment_serializer
from rest_framework.response import Response
from rest_framework.views import APIView
User = get_user_model()


def set_amount_view(request):
    user = request.user
    if request.method == 'POST':
        form = SetAmountForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            account_balance = get_withdrawable_balance(
                user) + get_deposit_balance(user)
            print(account_balance)
            if account_balance < obj.amount:
                return render(request, 'setamount.html', {'form': form, 'error': "please add money"})

            if obj.amount < 50:
                return render(request, 'setamount.html', {'form': form, 'error': "you can not add less than 50"})

            obj.save()
            if get_deposit_balance(user) >= obj.amount:
                patch_deposit_balance(user, -obj.amount)
                deduct_deposit_payment(user.id, obj.id, obj.amount)
                obj.user_payment = True
                obj.save()

            elif get_deposit_balance(user) < obj.amount:
                balance_to_withdrawn = get_deposit_balance(user)-obj.amount

                deduct_deposit_payment(
                    user.id, obj.id, get_deposit_balance(user))
                patch_deposit_balance(user, -get_deposit_balance(user))
                patch_withdrawble_balance(user, balance_to_withdrawn)
                deduct_withdrawl_payment(
                    user.id, obj.id, -balance_to_withdrawn)
                obj.user_payment = True
                obj.save()

            return redirect('/')
    else:
        form = SetAmountForm()
    return render(request, 'setamount.html', {'form': form})


def RoomCode(request):
    return render(request, 'room.html')


def home(request):
    # match = Price.objects.all().order_by('-amount')
    if not request.user.is_authenticated:
    # Handle unauthenticated users
       data = None  # Set data to None for unauthenticated users
    else:
    # Handle authenticated users
       user_id = request.user.id
       bal = get_withdrawable_balance(user_id) + get_deposit_balance(user_id)
       data = bal

    return render(request, 'home.html', {'data': data})



def ViewRoom(request):
    return render(request, 'viewroom.html')


class viewData(APIView):
    def get(self, request, id):
        if Room.objects.filter(room_id_id=id):
            room = Room.objects.filter(room_id_id=id)
            serlizsr = RoomSerializier(room, many=True).data
            data = serlizsr[0]['room_code']
            print(data)
            return Response(data)
        else:
            return Response(status=400)


class approval_request(APIView):

    # return Price.objects.get(id=pk)

    def patch(self, request, id):
        price = Price.objects.get(id=id)
        user = request.user
        ser_data = PriceSerializier(price).data
        if ser_data['request_to_join']:
            return Response(status=400)
        account_balance = get_withdrawable_balance(
            user) + get_deposit_balance(user)
        if account_balance < ser_data['amount']:
            return Response(status=409)

        data = {
            'request_to_join': True,
            'joined_by': user.id,
            'joined_user_payment': True
        }

        serializer = PriceSerializier(price, data=data, partial=True)
        if serializer.is_valid():
            if get_deposit_balance(user.id) >= ser_data['amount']:
                patch_deposit_balance(user.id, -ser_data['amount'])
                deduct_deposit_payment(user.id, id, ser_data['amount'])

            elif get_deposit_balance(user.id) < ser_data['amount']:
                balance_to_withdrawn = get_deposit_balance(
                    user.id)-ser_data['amount']
                deduct_deposit_payment(
                    user.id, id, get_deposit_balance(user.id))
                patch_deposit_balance(user.id, -get_deposit_balance(user.id))
                patch_withdrawble_balance(user.id, balance_to_withdrawn)
                deduct_withdrawl_payment(user.id, id, -balance_to_withdrawn)
            serializer.save()
            return Response(serializer.data)


class accept_reject_view(APIView):

    def patch(self, request, id):
        price = Price.objects.get(id=id)
        user = request.user
        ser_data = PriceSerializier(price).data
        # j1 = ser_data['joined_by']

        # j2=User.objects.get(id=j1)
        # join_serliazer=UserSerializer(j2).data['id']
        if request.data.get('rejected'):
            serializer = PriceSerializier(
                price, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)

        if ser_data['user'] != user.id:
            return Response(status=400)

        serializer = PriceSerializier(price, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


def check_result(id, user):
    if (result_win.objects.filter(result_id_id=id, won=user).exists() or result_loss.objects.filter(result_id_id=id, lost=user).exists() or result_cancel.objects.filter(result_id_id=id, cancel=user).exists() == True):
        return True


class result_win_view(APIView):
    def get(self, request, id):
        user = request.user
        result_win.objects.get(result_id_id=id, won=user.id)
        return Response(status=200)

    def post(self, request, id):
        print('post', type(request.data.get('img')))
        user = request.user
        pi = Price.objects.get(id=id)
        serializer_id = PriceSerializier(pi).data
        result_id = serializer_id['id']
        if check_result(id, user.id) == True:
            return Response(status=400)
        data = {
            'result_id': result_id,
            'won': user.id,
            'img': request.data.get('img')
        }

        ser = Resut_Win_Serializer(data=data)

        if not ser.is_valid():
            # Print the validation errors to debug
            print('Errors:', ser.errors)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=200)
        return Response(ser.errors, status=400)


class result_loss_view(APIView):

    def get(self, request, id):
        user = request.user

        result_loss.objects.get(result_id_id=id, lost=user.id)
        return Response(status=200)

    def post(self, request, id):
        user = request.user
        pi = Price.objects.get(id=id)
        serializer_id = PriceSerializier(pi).data
        result_id = serializer_id['id']

        if check_result(id, user.id) == True:
            return Response(status=400)
        data = {
            'result_id': result_id,
            'lost': user.id,

        }

        ser = Resut_Loss_Serializer(data=data)
        if not ser.is_valid():
            print(ser.errors)
        if ser.is_valid():
            ser.save()
            return Response(status=200)


class result_cancel_view(APIView):

    def get(self, request, id):
        user = request.user
        result_cancel.objects.get(result_id_id=id, cancel=user.id)
        return Response(status=200)

    def post(self, request, id):
        user = request.user
        pi = Price.objects.get(id=id)
        serializer_id = PriceSerializier(pi).data
        result_id = serializer_id['id']
        if check_result(id, user.id) == True:
            print('true')
            return Response(status=400)
        data = {
            'result_id': result_id,
            'cancel': user.id,

        }
        ser = Result_cancel_Serializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response(status=200)


# pyment deduct from palyers for match view

def get_payment_deposit_func(user, id):
    pi = match_deposit_payment.objects.get(user=user, price_model_id=id)
    pi_data = Match_deposit_payment_serializer(pi).data['amount']
    return pi_data


def get_payment_withdrwal_func(user, id):
    pi = match_withdrawl_payment.objects.get(user=user, price_model_id=id)
    pi_data = Match_withdrawal_payment_serializer(pi).data['amount']

    return pi_data


def deduct_deposit_payment(user, id, amount):
    if match_deposit_payment.objects.filter(user=user, price_model_id=id).exists():
        match_deposit_payment.objects.filter(
            user=user, price_model_id=id).update(amount=0)
        return
    data = {
        'user': user,
        'price_model': id,
        'amount': amount
    }
    print('vv', data)
    ser = Match_deposit_payment_serializer(data=data)
    if ser.is_valid():
        ser.save()


def deduct_withdrawl_payment(user, id, amount):
    if match_withdrawl_payment.objects.filter(user=user, price_model_id=id).exists():
        match_withdrawl_payment.objects.filter(
            user=user, price_model_id=id).update(amount=0)
        return
    data = {
        'user': user,
        'price_model': id,
        'amount': amount
    }
    print('zz', data)
    ser = Match_withdrawal_payment_serializer(data=data)
    if ser.is_valid():
        ser.save()

# staff duties views


class staffUser(APIView):
    permission_classes = [check_is_staff]

    def get(self, request):
        price = Price.objects.all()
        ser = PriceSerializier(price, many=True).data
        return Response(ser)


def staff_user(request):
    return render(request, 'staff.html')

def check_match(request):
    return render(request , 'check_match.html')


# refund views

class cancel_refund(APIView):
    permission_classes=[check_is_staff]
    def get(self, requst, id):
        price = Price.objects.get(id=id)
        ser = PriceSerializier(price).data
        created_by = ser['user']
        joined_by = ser['joined_by']

        #add adn deduct balance of created user

        patch_deposit_balance(
            created_by, get_payment_deposit_func(created_by, id))
        deduct_deposit_payment(
            created_by, id, -get_payment_deposit_func(created_by, id))
        
           #withdrwable

        if match_withdrawl_payment.objects.filter(user=created_by, price_model_id=id).exists():

            patch_withdrawble_balance(
                created_by, get_payment_withdrwal_func(created_by, id))
            deduct_withdrawl_payment(
                created_by, id, -get_payment_withdrwal_func(created_by, id))
            

        # add and deduct balance of joined user
        patch_deposit_balance(
            joined_by, get_payment_deposit_func(joined_by, id))
        deduct_deposit_payment(
            joined_by, id, -get_payment_deposit_func(joined_by, id))
        
               #withdrwable
        
        
        if match_withdrawl_payment.objects.filter(user=joined_by, price_model_id=id).exists():
            patch_withdrawble_balance(
                joined_by, get_payment_withdrwal_func(joined_by, id))
            deduct_withdrawl_payment(
                joined_by, id, -get_payment_withdrwal_func(joined_by, id))

        return Response(status=200)


# win money transefer view

class win_money_transefer_view(APIView):
    # permission_classes=[check_is_staff]

    def get(self , request , id):
        pi =Price.objects.get(id=id)
        data=PriceSerializier(pi).data['id']
        win_pi=result_win.objects.filter(result_id=data)
        win_data=Resut_Win_Serializer(win_pi ,many=True).data
        print('jhg',win_data)
        return Response(status=200)