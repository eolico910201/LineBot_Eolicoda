import os, json, random, time

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('9s1z4LRXBjXJbWjspPAtxyL1tER6EiwK+lhg/Rq1tUaSmh3uRbC5gi7TaM+99tnsnlvgiPPCJWwY+8VCcRi0rthnedKJD9fh23PqZZyf28lJh0O/LL6AS24Efq58c3el0PcuNP1hrCloybN2ChucMQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('df0b3a4ecb874a0727a45a8456ec6991')

def check_friend(usid):
    try:
        pof = line_bot_api.get_profile(usid)
        return pof
    except:
        return False

class user():
    def __init__(self, usid):
        data = usid + ".json"
        if os.path.isfile(data):
            with open(data, 'r') as f:
                x = json.load(f)
                self.level = x["level"]
                self.exp = x["exp"]
                self.name = x["name"]
        else:
            self.level = 1
            self.exp = 0
            pof = check_friend(usid)
            if pof:
                self.name = pof.display_name
            else:
                self.name = ""
        self.txt = []
        self.exp_up(usid, 1)
        self.save(usid)

    def save(self, usid):
        data = usid + ".json"
        x = {
                "level" : self.level,
                "exp" : self.exp,
                "name" : self.name
            }
        with open(data, 'w') as f:
            json.dump(x, f)
    
    def reply(self, rptoken):
        msg = []
        for i in self.txt:
            msg.append(TextSendMessage(text = i))
        self.txt = []
        line_bot_api.reply_message(rptoken, msg)

    def exp_up(self, usid, num):
        self.exp += num
        up = False
        while self.exp >= pow(self.level, 2) + 10:
            self.exp -= pow(self.level, 2) + 10
            self.level += 1
            up = True
        if up:
            self.txt.append("%s 等級提升到 %d 等!" % (self.name,self.level))




# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.type == 'text':
        rptoken = event.reply_token
        usid = event.source.user_id
        us = user(usid)
        msg = event.message.text
        if "你好" in msg or "妳好" in msg:
            us.txt.append("妳好啊! %s" % (us.name))
            us.reply(rptoken)
        elif msg == "#level":
            us.txt.append("%s\nlevel -> %d \nexp -> %d" % (us.name, us.level, us.exp))
            us.reply(rptoken)
        elif "#rename " in msg:
            tt = msg.split()
            name = ""
            for i in range(1,len(tt)):
                if i > 1:
                    name += " "
                name += tt[i]
            us.name = name
            us.save(usid)
            us.txt.append("%s\n名字已更新完畢" % (us.name))
            us.reply(rptoken)
        elif msg == "自爆" or msg == "友盡":
            if us.level < 5:
                us.txt.append("你太弱了!")
            else:
                us.level = 1; us.exp = 0
                us.save(usid)
                if event.source.type == "group":
                    gpid = event.source.group_id
                    us.txt.append("再...再見")
                    us.reply(rptoken)
                    line_bot_api.leave_group(gpid)
                else:
                    us.txt.append("你...你怎麼這樣對我")
                    us.reply(rptoken)
        try:
            us.reply(rptoken)
        except:
            pass

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)