from .serializers import PriceSerializier, PrcieCutSerializer, RoomSerializier, UserSerializer
from ludo.models import Price, Price_cut, Room
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']
        username = self.scope["user"]
        print('username', username)
        print(self.room_group_name, self.channel_name, self.user)

        # Join room Group

        # await self.get_room()
        if username:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()

    async def disconnect(self, close_code):

        self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        print('dddd',self,text_data)
        data = json.loads(text_data)
        command = data['command']

        if command == 'fetch_data':
            await self.fetch_data()

    async def fetch_data(self):
        username = self.scope['user']
        data_list = await self.fetch_data_from_db(username)
        price_waiting = await self.fetch_price_waiting(username)
        data_price = await self.fetch_data_from_db_price()
        user_price = await self.fetch_user_data_price(username)
        user_name = await self.fetch_username(username)
        user_request_price = await self.fetch_user_request_data_price(username)
        
        my_user_data=await self.fetch_my_user_data_price(username)
        accept_to_play = await self.fetch_accept_to_paly(username)


        await self.send(text_data=json.dumps({'data': data_list, 'price_waiting': price_waiting, 'accept_to_play': accept_to_play,'my_data':my_user_data, 'price': data_price, 'user_price': user_price, 'username': user_name, 'request_price': user_request_price}))

    # main data
    @staticmethod
    @sync_to_async
    def fetch_data_from_db(username):
        data = Price.objects.order_by(
            '-amount').exclude(user=username).exclude(request_to_join=True)
        serlizerData = PriceSerializier(data, many=True).data
        return list(serlizerData)

    # user waiting data

    @staticmethod
    @sync_to_async
    def fetch_price_waiting(username):
        data = Price.objects.filter(
            user=username, request_to_join=False).exclude(closed=True)
        serlizerData = PriceSerializier(data, many=True).data
        return serlizerData

    # request to paly accepted

    @staticmethod
    @sync_to_async
    def fetch_accept_to_paly(username):
        data = Price.objects.filter(
            joined_by=username).exclude(closed=True)
        serlizerData = PriceSerializier(data, many=True).data
        return serlizerData

    @staticmethod
    @sync_to_async  # Price cut
    def fetch_data_from_db_price():
        data = Price_cut.objects.all()
        serlizerData = PrcieCutSerializer(data, many=True).data
        return list(serlizerData)

    @staticmethod
    @sync_to_async
    def fetch_user_data_price(username):
        data = Price.objects.filter(user=username).exclude(closed=True)
        serlizerData = PriceSerializier(data, many=True).data
        return list(serlizerData)

    # user request
    @staticmethod
    @sync_to_async
    def fetch_user_request_data_price(username):
        data = Price.objects.filter(user=username, request_to_join=True).exclude(
            accetp_to_play=True).exclude(rejected=True).exclude(closed=True)
        serlizerData = PriceSerializier(data, many=True).data
        print('requested',serlizerData)
        return list(serlizerData)
    
    # view my room
    @staticmethod
    @sync_to_async
    def fetch_my_user_data_price(username):
        data = Price.objects.filter(user=username,accetp_to_play=True).exclude(closed=True)
        serlizerData = PriceSerializier(data, many=True).data
        return list(serlizerData)

    @staticmethod
    @sync_to_async
    def fetch_username(username):
        data = User.objects.get(username=username)
        serlizerData = UserSerializer(data).data['username']
        return serlizerData




class ChatMessage(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        # Join room Group

        # await self.get_room()
        self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await (self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        id = text_data_json['id']

        type = text_data_json['type']

        # Send message to room group
        if type == 'chat_message':
            await self.create_message(id, message)

            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message", "message": message, 'id': id}
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        id = event['id']

        # Send message to WebSocket
        self.send(text_data=json.dumps(
            {"message": message, 'id': self.room_name}))
        self.create_message(id, message)

    @sync_to_async
    def create_message(self, id, message):
        pi = Price.objects.get(id=id)
        serializer_id = PriceSerializier(pi).data
        room_id = serializer_id['id']

        Room.objects.create(room_id_id=room_id,  room_code=message)


