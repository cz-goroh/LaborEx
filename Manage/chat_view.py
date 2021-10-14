import json, logging, datetime, os, logging, base64
from aiohttp import web, ClientSession, WSMsgType
from django.apps import apps
from django.conf import settings
from channels.db import database_sync_to_async
# from django.conf import settings
from django.core.files.base import ContentFile

logging.basicConfig(filename="task_book.log", level=logging.INFO)

class MixView():

    def get_m(self, model_name):
        model_obj = apps.get_model(model_name)
        return model_obj

    @database_sync_to_async
    def new_mes(self, text, user_from, user_to, file, filename=None):
        User = self.get_m(settings.AUTH_USER_MODEL)
        Message = self.get_m('Manage.Message')
        mes = Message(
            user_from=User.objects.get(pk=user_from),
            user_to=User.objects.get(pk=user_to),
            text=text,
        )
        mes.save()
        if file:
            head, data = file.split(',')
            # decoded =data.decode('base64','strict');
            # print(head)
            print(filename)
            fl = ContentFile(base64.b64decode(data), name=filename)
            mes.file = fl
            mes.save()
        return mes


class WSch(web.View, MixView):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        async for msg in ws:
            # print(self.request.app.wslist)
            # print(msg.type)

            mes_dict = json.loads(msg.data)
            if not mes_dict:
                print(mes_dict)
                await ws.send_json(True)
                # print('ping')
            elif mes_dict['text'] or mes_dict['file']:
                mes = await self.new_mes(
                    mes_dict['text'],
                    mes_dict['user_from'],
                    mes_dict['user_to'],
                    mes_dict['file'],
                    mes_dict['filename']
                    # None # сейчас файл не передаём
                )
                await self.broadcast_to_once_peer(mes)
                # if mes_dict['user_from'] not in self.request.app.wslist:
                self.request.app.wslist[mes_dict['user_from']] = ws

    async def broadcast_to_once_peer(self, mes):
        """# TODO: реализовать историю с прочитанными/непрочитанными сообщениями и с
        уведомлением о непрочитанных сообщениях при подключении пира"""
        # for us, peer in self.request.app.wslist[mes]
        # print(mes)
        if mes.user_to.id in self.request.app.wslist:
            peer = self.request.app.wslist[mes.user_to.id]
            avatar = None
            text = mes.text
            if mes.file:
                text = f'{mes.text} приложено: <a href="{mes.file.url}">{mes.file.url}</a>'
                print(text)
            try:
                await peer.send_json({
                    'text': text,
                    'from_name': mes.user_from.username,
                    'time': mes.sent_time.strftime("%d.%m.%Y, %H:%M:%S"),
                    'avatar': avatar
                })
            except Exception as e:
                print(e)
                await peer.close()
                self.request.app.wslist.pop(mes.user_from.id)


class WSChat(web.View, MixView):

    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        async for msg in ws:
            # print(self.request.app.wslist) views

            if msg.type == WSMsgType.BINARY:
                print(msg.extra)
            else:
                mes_dict = json.loads(msg.data)
                # print(mes_dict)
                if mes_dict['text'] or mes_dict['file']:

                    mes = await self.new_mes(
                        mes_dict['text'],
                        mes_dict['room'],
                        mes_dict['user_id'],
                        mes_dict['file'],
                        mes_dict['filename']
                    )
                    await self.broadcast(mes)
                if mes_dict['room'] not in self.request.app.wslist:
                    self.request.app.wslist[mes_dict['room']] = {}
                self.request.app.wslist[mes_dict['room']][mes_dict['user_id']] = ws


    async def broadcast(self, mes):
        """ Send messages to all in this room
        # TODO: реализовать историю с прочитанными/непрочитанными сообщениями и с
        уведомлением о непрочитанных сообщениях при подключении пира
         """
        for us, peer in self.request.app.wslist[mes.room.id].items():
            try:
                avatar = None
                # if mes.from_user.avatar:
                #     avatar = mes.from_user.avatar.url
                text = mes.text
                if mes.file:
                    text = f'{mes.text} приложено: <a href="/media/{mes.file.url}">{mes.file.url}</a>'
                    print(text)
                await peer.send_json({
                'text':text,
                'from_name': mes.user_from.username,
                'time': mes.sent_time.strftime("%d.%m.%Y, %H:%M:%S"),
                'avatar': avatar
                })
            except Exception as e:
                # print(e)
                await peer.close()
                pass
