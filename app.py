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

def reply(rptoken, txt):
    msg = []
    for i in txt:
        msg.append(TextSendMessage(text = i))
    line_bot_api.reply_message(rptoken, msg)

def check_friend(mbid):
    try:
        pof = line_bot_api.get_profile(mbid)
        return pof
    except:
        return False

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
        txt = []
        rptoken = event.reply_token
        mbid = event.source.user_id
        flag = check_friend(mbid)
        msg = event.message.text
        if "你好" in msg or "妳好" in msg:
            if flag:
                txt.append("妳好啊! %s" % (flag.display_name))
                reply(rptoken, txt)
            else:
                txt.append("妳好啊!")
                reply(rptoken, txt)
        if event.source.type == "group":
            gpid = event.source.group_id
            if msg == "自爆" or msg =="友盡":
                if flag:
                    txt.append("再...再見")
                    reply(rptoken, txt)
                    line_bot_api.leave_group(gpid)
                else:
                    txt.append("你太弱了!")
                    reply(rptoken, txt)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
