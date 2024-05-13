import yfinance as yf
from datetime import datetime, timedelta
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

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

def get_stock_data(stock_code):
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    df = yf.Ticker(stock_code).history(start=start_date, end=end_date)
    df['Volume_Formatted'] = df['Volume'].apply(lambda x: '{:,.0f}'.format(x))
    df['Volume_Money'] = df['Volume'] * df['Close']
    df['Volume_Money_Formatted'] = df['Volume_Money'].apply(lambda x: '{:,.2f}'.format(x))
    return df

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
    if re.match('鴻海股票', message):
        stock_data = get_stock_data("2317.TW")
        response = "近一個月鴻海（2317.TW）股票歷史資料：\n" + stock_data.to_string()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
    elif re.match('告訴我秘密', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('才不告訴你哩！'))   
    elif re.match('睡', message):
        # 貼圖查詢：https://developers.line.biz/en/docs/messaging-api/sticker-list/#specify-sticker-in-message-object
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)
    # 其他條件...
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
