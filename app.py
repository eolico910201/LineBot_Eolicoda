<<<<<<< HEAD
<<<<<<< HEAD
import json, math

=======
>>>>>>> init
=======
import json, math

>>>>>>> basic
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('9s1z4LRXBjXJbWjspPAtxyL1tER6EiwK+lhg/Rq1tUaSmh3uRbC5gi7TaM+99tnsnlvgiPPCJWwY+8VCcRi0rthnedKJD9fh23PqZZyf28lJh0O/LL6AS24Efq58c3el0PcuNP1hrCloybN2ChucMQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('df0b3a4ecb874a0727a45a8456ec6991')

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> basic
class group():
    def __init__(self, gpid):
        data = gpid + ".json"
        if os.path.isfile(data):
            with open(data, "r") as f:
                x = json.load(f)
                self.gpid = x["gpid"]
                self.member = x["member"]
                f.close()
        else:
            self.gpid = gpid
            self.member = {}
        self.txt = []
    
    def save(self):
        data = self.gpid + ".json"
        x = {"gpid" : self.gpid,
             "member" : self.member}
        with open(data, "w") as f:
            json.dump(x, f)
            f.close()

    def reply(self, rptoken):
        message = []
        for i in self.txt:
            message.append(TextSendMessage(text = i))
        self.txt = []
        line_bot_api.reply_message(rptoken, message)
    
    def exp_up(self, mbid):
        if not mbid in self.member:
            self.member[mbid] = {"exp" : 1, "level" : 1}
        else:
            self.member[mbid]["exp"] += 1
            if self.member[mbid]["exp"] >= pow(self.member[mbid]["level"], 2) + 10:
                self.member[mbid]["exp"] = 0; self.member[mbid]["level"] += 1
                pof = line_bot_api.get_profile(mbid)
                self.txt.append("Level Up!")
                self.txt.append("%s 等級提升到 %d !" % (pof.display_name, self.member[mbid]["level"]))
        self.save()

<<<<<<< HEAD
=======
>>>>>>> init
=======
>>>>>>> basic
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> basic
    rptoken = event.reply_token
    if event.source.type == 'group':
        gpid = event.source.group_id
        mbid = event.source.user_id
        gp = group(gpid)
        gp.exp_up(mbid)
        if event.message.type == 'text':
            msg = event.message.text
            if msg == "自爆":
                if gp.member[mbid]["level"] >= 5:
                    gp.txt.append("再...再見")
                    gp.reply(rptoken)
                    line_bot_api.leave_group(gpid)
                else:
                    gp.txt.append("你太弱了!")
                    gp.reply(rptoken)
            else:
                if msg =="妳好" or msg == "你好":
                    pof = line_bot_api.get_profile(mbid)
                    gp.txt.append("你好 " + pof.display_name)
                elif msg == "#me":
                    pof = line_bot_api.get_profile(mbid)
                    x = gp.member[mbid]
                    gp.txt.append("name => %s\nlevel => %d\nexp => %d" % (pof.display_name,x["level"],x["exp"]))
<<<<<<< HEAD
                gp.reply(rptoken)             
=======
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)
>>>>>>> init
=======
                gp.reply(rptoken) 
>>>>>>> basic

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
<<<<<<< HEAD
    app.run(host='0.0.0.0', port=port)
=======
    app.run(host='0.0.0.0', port=port)
>>>>>>> init
