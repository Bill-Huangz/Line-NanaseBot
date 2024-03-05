from django.shortcuts import render

from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import configparser
import urllib.request as req
import json 
import requests
# Create your views here.
config = configparser.ConfigParser()
config.read('/mnt/d/Github/Line-NanaseBot/LineBot/splash/config.ini')

headers ={'Authorization': 'Client-ID '+ config.get('splash','access_ID')}
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
parser = WebhookParser(config.get('line-bot', 'channel_secret'))

@csrf_exempt
def callback(request):
    if request.method=='POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                unsplash_url='https://api.unsplash.com/photos/random'
                txt=event.message.text
                
                r=requests.get(unsplash_url, headers=headers)

                msg=[]
                img=ImageSendMessage(original_content_url=r.json()['urls']['regular'], preview_image_url=r.json()['urls']['small'])
                # msg.append(TextSendMessage(text=txt))
                msg.append(img)
                line_bot_api.reply_message(event.reply_token, msg)
        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
                