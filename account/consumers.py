import json
import requests

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.http import HttpResponse

from account.models import Thread, ChatMessage, User



class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('receive', event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        sent_by_id = received_data.get('sent_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')
        print('thread_idddd',thread_id)
        if not msg:
            print('Error:: empty message')
            return False

        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)

        print("sdhds",send_to_user.id)
        if not sent_by_user:
            print('Error:: sent by user is incorrect')
        if not send_to_user:
            print('Error:: send to user is incorrect')
        if not thread_obj:
            print('Error:: Thread id is incorrect')

        await self.create_chat_message(thread_obj.id, sent_by_user.id, msg)
        await self.chat_notification(thread_obj, sent_by_user, msg)

        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self_user = self.scope['user']
        response = {
            'message': msg,
            'sent_by': self_user.id,
            'thread_id': thread_id
        }

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )



    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def chat_message(self, event):
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        print('beforeeeeee',thread,user,msg)
        chat = ChatMessage.objects.create(thread_id=thread, user_id=user, message=msg)
        print('sfvbbrb',chat)
       

    
    # def send_notification(self, event):
    #     print("send notification")
    #     print('hnnnn',event)
    @database_sync_to_async
    def chat_notification(self,thread_obj, sent_by_user, msg):
        
        thread = thread_obj.first_person_id
        
        msgg = msg
        to_id = sent_by_user
        to_obj = User.objects.get(id=thread)
        token = to_obj.fcm_token
        print(token)
        
        
        fcm_api = "AAAAEzrWrBo:APA91bFb1gozb9_NNJ6XYQxfCrUsmZQIjGZDYRbInRELckVwcuK3DwFB6cP-SuWzC7a4-gYe_r1Sg9eNj6pDEsMSyZZ_C5Q4U4LDrlfST-ojxKmg1YBnBtahhRSRE8wT8rNWltfgnPag"
        url="https://fcm.googleapis.com/fcm/send"
        body={
            "notification":{
                "title":f"message from {to_id} ",
                "body":msg,
                "click_action": f"http://127.0.0.1:8000/chat/?name={to_id}",
            },
            "to":token
        }
        headers={"Content-Type":"application/json","Authorization":"key="+fcm_api}
        data=requests.post(url,data=json.dumps(body),headers=headers)
        
        print(data.text)
        return HttpResponse("True")
