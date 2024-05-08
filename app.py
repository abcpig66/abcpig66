# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 12:39:41 2019

@author: Ivan
"""
from fugle_realtime import intraday
import schedule
import time

# Line Bot部分
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

line_bot_api.push_message('Uae4d95a8996273cbd5fd013544cb3d5a', TextSendMessage(text='你可以開始了'))

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
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
    elif re.match('請求', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='4'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('美好', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='5'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('生氣', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='6'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('是你', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='7'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('怕', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='8'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('衰', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='9'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('笑', message):
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='10'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('關鍵字',message):
        flex_message = TextSendMessage(text='以下有雷，請小心',
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="關鍵價位", text="關鍵！")),
                                   QuickReplyButton(action=MessageAction(label="密碼", text="密碼！")),
                                   QuickReplyButton(action=MessageAction(label="到價", text="到價提醒！")),
                                   QuickReplyButton(action=MessageAction(label="重要筆記", text="重要！！")),
                                   QuickReplyButton(action=MessageAction(label="早安", text="早安！")),
                                   QuickReplyButton(action=MessageAction(label="歡迎", text="歡迎！")),
                                   QuickReplyButton(action=MessageAction(label="貼圖", text="笑！")),                               
                               ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif re.match('到價提醒',message): # 新增的部分
        stock_info = "目前監控的股票及其價格：\n"
        for i, j in zip(allstock, allprice):
            stock_info += f"{i}: {j}\n"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=stock_info))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

def stockPrice_check(stock, check_price):
    stockdf=intraday.trades(apiToken="p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=", 
                output="dataframe", 
                symbolId=stock)
    nowprice = stockdf['price'].values[-1]
    if nowprice > check_price:
        print(stock + ' 目前價格 ' + str(nowprice))
        
def job():
    allstock = ['2330','2002','2382']
    allprice = [805, 26 , 280]
    for i,j in zip(allstock, allprice):
        stockPrice_check(i, j)

second_5_j = schedule.every(3).seconds.do(job)

while True: 
    schedule.run_pending()
    time.sleep(1)
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)