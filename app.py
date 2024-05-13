# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第三章 互動回傳功能
傳送貼圖StickerSendMessage
"""
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
import openai

# 初始化 Flask app 和 Line Bot API
app = Flask(__name__)
line_bot_api = LineBotApi('p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('980186763ec26279c6c95254f44a4ae8')

# 设置 OpenAI API 密钥
openai.api_key = 'sk-proj-LmrAbLuviYLLfd3NTiwOT3BlbkFJpVONwvBXFuOYxe8WyBWY'

# 监听所有来自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # 获取 X-Line-Signature header 值
    signature = request.headers['X-Line-Signature']

    # 获取 request body 作为 text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 处理 webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#消息传递区块
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match('告訴我秘密', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('才不告訴你哩！'))
    elif re.match('睡', message):
        sticker_message = StickerSendMessage(package_id='1', sticker_id='1')
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('好', message):
        sticker_message = StickerSendMessage(package_id='1', sticker_id='2')
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('驚', message):
        sticker_message = StickerSendMessage(package_id='1', sticker_id='3')
        line_bot_api.reply_message(event.reply_token, sticker_message)
    # 继续新增其他贴纸...
    elif re.match('請求', message):
        sticker_message = StickerSendMessage(package_id='1', sticker_id='4')
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('美好', message):
        sticker_message = StickerSendMessage(package_id='1', sticker_id='5')
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('生氣', message):
        sticker_message = StickerSendMessage(package_id='1', sticker_id='6')
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('是你', message):
        sticker_message = StickerSendMessage(package_id='1', sticker_id='7')
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('怕', message):
        sticker_message = StickerSendMessage(package_id='1', sticker_id='8')
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('衰', message):
        sticker_message = StickerSendMessage(package_id='1', sticker_id='9')
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('笑', message):
        sticker_message = StickerSendMessage(package_id='1', sticker_id='10')
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('關鍵字',message):
        flex_message = TextSendMessage(text='以下有雷，請小心',
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="關鍵價位", text="關鍵！")),
                                   QuickReplyButton(action=MessageAction(label="密碼", text="密碼！")),
                                   QuickReplyButton(action=MessageAction(label="木沐", text="木沐！")),
                                   QuickReplyButton(action=MessageAction(label="重要筆記", text="重要！！")),
                                   QuickReplyButton(action=MessageAction(label="早安", text="早安！")),
                                   QuickReplyButton(action=MessageAction(label="歡迎", text="歡迎！")),
                                   QuickReplyButton(action=MessageAction(label="貼圖", text="笑！")),                               
                               ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('台積電',message):
        # 使用 OpenAI 对话模型获取回复
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 或者你选择的其他模型
            messages=[
                {"role": "system", "content": "You are a chatbot."},
                {"role": "user", "content": message}
            ]
        )
        # 提取 OpenAI 模型的回复
        ai_response = completion.choices[0].message['content']
        line_bot_api.reply_message(event.reply_token, TextSendMessage(ai_response))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
