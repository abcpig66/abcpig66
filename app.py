# -*- coding: utf-8 -*-
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('980186763ec26279c6c95254f44a4ae8')

line_bot_api.push_message('Uae4d95a8996273cbd5fd013544cb3d5a', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('睡',message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('好', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='2'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('驚', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='3'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif message == 'POST':
        # 回覆所有 POST 資訊
        post_data = request.get_data(as_text=True)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(post_data))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
      
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)