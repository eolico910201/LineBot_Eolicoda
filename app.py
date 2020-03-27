import os, json

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

class group():
    def __init__(self, gpid, usid):
        data = gpid + ".json"
        if os.path.isfile(data):
            with open(data, 'r') as f:
                x = json.load(f)
                self.member = x["member"]
        else:
            self.member = {}
        self.txt = []
        self.exp_up(usid)

    def save(self, gpid):
        data = gpid + ".json"
        x = {"member" : self.member}
        with open(data, 'w') as f:
            json.dump(x, f)
    
    def reply(self, rptoken):
        msg = []
        for i in self.txt:
            msg.append(TextSendMessage(text = i))
        self.txt = []
        line_bot_api.reply_message(rptoken, msg)

    def exp_up(self, usid):
        if usid in self.member:
            x = self.member[usid]
            x["exp"] += 1
            if x["exp"] >= pow(x["level"], 2) + 10:
                x["level"] +=1; x["exp"] = 0
                pof = check_friend(usid)
                if pof:
                    self.txt.append("%s 等級提升到 %d 等!" % (pof.display_name,x["level"]))
            self.member[usid] = x
        else:
            self.member[usid] = {"level" : 1, "exp" : 1}


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
        flag = check_friend(usid)
        msg = event.message.text
        if event.source.type == "group":
            gpid = event.source.group_id
            gp = group(gpid, usid)
            if msg == "自爆" or msg =="友盡":
                if flag:
                    gp.txt.append("再...再見")
                    gp.reply(rptoken)
                    line_bot_api.leave_group(gpid)
                else:
                    gp.txt.append("你太弱了!")
                    gp.reply(rptoken)
            else:
                if "你好" in msg or "妳好" in msg:
                    if flag:
                        gp.txt.append("妳好啊! %s" % (flag.display_name))
                    else:
                        gp.txt.append("妳好啊!")
                elif msg == "#level":
                    if flag:
                        x = gp.member[usid]
                        gp.txt.append("%s\nlevel -> %d \nexp -> %d" %(flag.display_name, x["level"], x["exp"]))
                    else:
                        gp.txt.append("加入好友解鎖功能")
                try:
                    gp.reply(rptoken)
                except:
                    pass
            gp.save(gpid)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
