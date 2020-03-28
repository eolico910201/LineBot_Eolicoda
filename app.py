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

class group():
    def __init__(self, gpid, usid):
        data = gpid + ".json"
        if os.path.isfile(data):
            with open(data, 'r') as f:
                x = json.load(f)
                self.member = x["member"]
                self.hp = x["hp"]
                #self.dmg_cd = x["dmg_cd"]
        else:
            self.member = {}
            self.hp = 10000
            self.death = False
            #self.dmg_cd = {}
        self.txt = []
        self.flag = check_friend(usid)
        self.exp_up(usid, 1)
        self.save(gpid)

    def save(self, gpid):
        data = gpid + ".json"
        x = {
             "member" : self.member,
             "hp" : self.hp
             #"dmg_cd" : self.dmg_cd
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
        if usid in self.member:
            x = self.member[usid]
            x["exp"] += num
        else:
            x = {"level" : 1, "exp" : num}
        up = False
        while x["exp"] >= pow(x["level"], 2) + 10:
            x["exp"] -= pow(x["level"], ) + 10
            x["level"] += 1
            up = True
        if self.flag and up:
            self.txt.append("%s 等級提升到 %d 等!" % (self.flag.display_name, x["level"]))
        self.member[usid] = x
    
    def damage(self, gpid, usid, typ):
        x = self.member[usid]
        dmg = random.randint(5000,10000)
        sd = random.choice(["","爆擊"])
        if sd == "爆擊":
            dmg *= (1.2 + x["level"]*0.1)
            dmg = int(dmg)
        self.hp -= dmg
        if self.hp <= 0:
            self.txt.append("我選擇死亡!")
            #self.exp_up(usid, 75)
            self.hp = 10000
            self.death = True
            #self.dmg_cd = 
        else:
            tt = "不要再打我啦!\n\n%s 打出了 %d點%s%s傷害!" % (self.flag.display_name, dmg, sd, typ)
            self.txt.append(tt + "\n\n剩餘血量 : %d點" % (self.hp))
        self.save(gpid)





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
        msg = event.message.text
        if event.source.type == "group":
            gpid = event.source.group_id
            gp = group(gpid, usid)
            if msg == "#魔法攻擊" or msg == "#物理攻擊":
                if gp.flag:
                    gp.damage(gpid, usid, msg[0:2])
                else:
                    gp.txt.append("你無法與我為敵!")
            elif "野" in msg:
                s = ""
                for i in msg:
                    if i == "野":
                        s += "格"
                    else:
                        s += i
                gp.txt.append(s)
            elif msg == "自爆" or msg =="友盡":
                if gp.flag:
                    gp.txt.append("再...再見")
                    gp.death = True
                else:
                    gp.txt.append("你太弱了!")
            elif "你好" in msg or "妳好" in msg:
                if gp.flag:
                    gp.txt.append("妳好啊! %s" % (gp.flag.display_name))
                else:
                    gp.txt.append("妳好啊!")
            elif msg == "#level":
                if gp.flag:
                    x = gp.member[usid]
                    gp.txt.append("%s\nlevel -> %d \nexp -> %d" %(gp.flag.display_name, x["level"], x["exp"]))
                else:
                    gp.txt.append("加入好友解鎖功能")
            gp.reply(rptoken)
            if gp.death:
                line_bot_api.leave_group(gpid)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
