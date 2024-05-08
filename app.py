# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第三章 互動回傳功能
傳送貼圖StickerSendMessage
"""
import requests
import json
import time
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

line_bot_api = LineBotApi('p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('980186763ec26279c6c95254f44a4ae8')

# 證交所 API 請求函式
def get_stock_price(stock_code):
    url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210507&stockNo={stock_code}"
    response = requests.get(url)
    data = response.json()
    return data

# 訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('睡', message):
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
    # 繼續新增其他貼圖...
    elif re.match('鴻海價格', message):
        stock_data = get_stock_price('2317')
        latest_price = float(stock_data['data'][0][6])  # 最近收盤價
        if latest_price >= 170:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="鴻海股價已達到或超過170元"))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="鴻海股價未達到170元"))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
       
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 主程式
if __name__ == "__main__":
    # 開啟 Flask 伺服器
    app.run(host='0.0.0.0', port=5000)
