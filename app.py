# -*- coding: utf-8 -*-
"""
創建於 2021年6月2日 21:16:35

作者：Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡 ivanyang0606@gmail.com

Line Bot 聊天機器人
第三章 互動回傳功能
傳送貼圖 StickerSendMessage
"""
# 載入所需的套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import re
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
import json

app = Flask(__name__)

# 必須放上自己的 Channel Access Token
line_bot_api = LineBotApi('p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的 Channel Secret
handler = WebhookHandler('980186763ec26279c6c95254f44a4ae8')

# 發送訊息給用戶（測試用）
line_bot_api.push_message('Uae4d95a8996273cbd5fd013544cb3d5a', TextSendMessage(text='你可以開始了'))

# 定義回調路徑
@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature 標頭值
    signature = request.headers['X-Line-Signature']

    # 獲取請求主體內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 處理 webhook 主體
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 定義訊息處理函數
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    response = None

    # 設置日期提醒
    match = re.match(r'提醒我在 (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) 說 (.+)', message)
    if match:
        remind_time = match.group(1)
        remind_message = match.group(2)

        try:
            remind_datetime = datetime.strptime(remind_time, '%Y-%m-%d %H:%M')
            add_reminder(event.source.user_id, remind_datetime, remind_message)
            response = TextSendMessage(f'好的，我會在 {remind_time} 提醒你：{remind_message}')
        except ValueError:
            response = TextSendMessage('請輸入正確的日期時間格式，例如：2024-06-01 14:00')

    if response:
        line_bot_api.reply_message(event.reply_token, response)

# 定義整點提醒功能
def hourly_reminder():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"現在時間是 {now}，整點提醒！"
    # 替換為實際的用戶 ID
    line_bot_api.push_message('Uae4d95a8996273cbd5fd013544cb3d5a', TextSendMessage(text=message))

# 設置定時任務
scheduler = BackgroundScheduler()
scheduler.add_job(hourly_reminder, 'cron', minute=0)
scheduler.start()

# 定義增加提醒功能
def add_reminder(user_id, remind_datetime, message):
    # 動態創建定時任務
    scheduler.add_job(
        func=send_reminder,
        trigger=DateTrigger(run_date=remind_datetime),
        args=[user_id, message],
        id=f"{user_id}_{remind_datetime.strftime('%Y%m%d%H%M%S')}",
        replace_existing=True
    )

# 定義發送提醒功能
def send_reminder(user_id, message):
    line_bot_api.push_message(user_id, TextSendMessage(text=message))

# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
