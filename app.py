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
import pytz

app = Flask(__name__)

# 必須放上自己的 Channel Access Token
line_bot_api = LineBotApi('p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的 Channel Secret
handler = WebhookHandler('980186763ec26279c6c95254f44a4ae8')

line_bot_api.push_message('Uae4d95a8996273cbd5fd013544cb3d5a', TextSendMessage(text='你可以開始了'))

# 設定台北時區
taipei_tz = pytz.timezone('Asia/Taipei')

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

# 訊息傳遞區塊
##### 基本上程式編輯都在這個 function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match('告訴我秘密', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('才不告訴你哩！'))
    elif re.match('睡', message):
        # 貼圖查詢：https://developers.line.biz/en/docs/messaging-api/sticker-list/#specify-sticker-in-message-object
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('好', message):
        # 新增第二個貼圖
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='2'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif re.match('驚', message):
        # 新增第三個貼圖
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='3'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    # 繼續新增其他貼圖...
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
                                   QuickReplyButton(action=MessageAction(label="木沐", text="木沐！")),
                                   QuickReplyButton(action=MessageAction(label="重要筆記", text="重要！！")),
                                   QuickReplyButton(action=MessageAction(label="早安", text="早安！")),
                                   QuickReplyButton(action=MessageAction(label="歡迎", text="歡迎！")),
                                   QuickReplyButton(action=MessageAction(label="貼圖", text="笑！")),                               
                               ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    # 設置日期提醒
    elif re.match(r'提醒我在 (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) 說 (.+)', message):
        match = re.match(r'提醒我在 (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) 說 (.+)', message)
        remind_time = match.group(1)
        remind_message = match.group(2)

        try:
            remind_datetime = datetime.strptime(remind_time, '%Y-%m-%d %H:%M')
            remind_datetime = taipei_tz.localize(remind_datetime)
            add_reminder(event.source.user_id, remind_datetime, remind_message)
            response = TextSendMessage(f'好的，我會在 {remind_time} 提醒你：{remind_message}')
        except ValueError:
            response = TextSendMessage('請輸入正確的日期時間格式，例如：2024-06-01 14:00')
        
        line_bot_api.reply_message(event.reply_token, response)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

# 定義整點提醒功能
def hourly_reminder():
    now = datetime.now(taipei_tz).strftime("%Y-%m-%d %H:%M:%S")
    message = f"現在時間是 {now}，整點提醒！"
    # 替換為實際的用戶 ID
    line_bot_api.push_message('Uae4d95a8996273cbd5fd013544cb3d5a', TextSendMessage(text=message))

# 設定定時任務
scheduler = BackgroundScheduler()
scheduler.add_job(hourly_reminder, 'cron', minute=0, timezone=taipei_tz)
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

# 增加特定日期的提醒通知
def add_specific_date_reminders():
    user_id = 'Uae4d95a8996273cbd5fd013544cb3d5a'
    remind_dates = [
        "2024-06-02", "2024-06-05", "2024-06-08", "2024-06-10",
        "2024-06-14", "2024-06-15", "2024-06-16", "2024-06-17",
        "2024-06-20", "2024-06-22", "2024-06-24", "2024-06-25",
        "2024-06-26", "2024-06-27", "2024-06-29", "2024-06-30"
    ]
    for date_str in remind_dates:
        remind_datetime = taipei_tz.localize(datetime.strptime(date_str + " 09:00", '%Y-%m-%d %H:%M'))
        message = f"提醒你今天要上班！{date_str}"
        add_reminder(user_id, remind_datetime, message)

# 主程式
if __name__ == "__main__":
    add_specific_date_reminders()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
