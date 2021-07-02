import __init__
import os
import ssl
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from conf import settings



ssl._create_default_https_context = ssl._create_unverified_context

class SlackSender(object):
    def __init__(self):
        self.client = WebClient(token=settings.slack_token)
        self.channel = settings.slack_channel
        self.channel_image = settings.slack_channel_image

    def send_msg(self,msg):
        try:
            response = self.client.chat_postMessage(channel=self.channel,text=msg[0]["text"]["text"],blocks=msg,as_user=True)
            #print(response)
            assert response["message"]["text"] == msg[0]["text"]["text"]
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")

    def upload_file(self,file_path):
        try:
            response = self.client.files_upload(channels=self.channel_image,file=file_path)
            assert response["file"]
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")
        print(response)
        return response


if __name__ == '__main__':
    SLK = SlackSender()
    SLK.upload_file('image/cover.jpg')
