import base64
import hashlib
import hmac
import json
import time
import urllib
from urllib import parse

import requests


class sendNotify:

    def ddBotNotify(text):
        DD_BOT_TOKEN = 'da303b4aa4112a529c78a07b7aa99517ba38be2f72cf789cc07202ff49b9c441'
        # 密钥，机器人安全设置页面，加签一栏下面显示的SEC开头的字符串
        DD_BOT_SECRET = 'SEC89d6946b7943f491e94c2307834e33d1318ae10f7af4f85b806f112a0a7caeac'
        if DD_BOT_TOKEN != '':
            url = 'https://oapi.dingtalk.com/robot/send?access_token=' + DD_BOT_TOKEN
            data = {
                "msgtype": "text",
                "text": {
                    'content': text
                }
            }
            headers = {
                'Content-Type': 'application/json;charset=utf-8'
            }
            if DD_BOT_TOKEN != '' and DD_BOT_SECRET != '':
                timestamp = str(round(time.time() * 1000))
                secret_enc = DD_BOT_SECRET.encode('utf-8')
                string_to_sign = '{}\n{}'.format(
                    timestamp, DD_BOT_SECRET)
                string_to_sign_enc = string_to_sign.encode('utf-8')
                hmac_code = hmac.new(
                    secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
                sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
                url = 'https://oapi.dingtalk.com/robot/send?access_token=' + \
                      DD_BOT_TOKEN + '&timestamp=' + timestamp + '&sign=' + sign

            response = requests.post(
                url=url, data=json.dumps(data), headers=headers).text
            if json.loads(response)['errcode'] == 0:
                print('\n钉钉发送通知消息成功\n')
            else:
                print('\n发送通知失败！！\n')
        else:
            print('\n您未提供钉钉的有关数据，取消钉钉推送消息通知\n')
            pass


def send(msg):
    title = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "健康打卡结果：\n" + msg
    sendNotify.ddBotNotify(title)
