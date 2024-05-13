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

line_bot_api = LineBotApi('p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('980186763ec26279c6c95254f44a4ae8')

def get_stock_data():
    # 獲取當前日期
    end_date = datetime.today().strftime('%Y-%m-%d')
    # 計算開始日期（一個月前）
    start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    # 從 Yahoo Finance 上獲取鴻海（2317.TW）股票的近一個月歷史資料
    df = yf.Ticker("2317.TW").history(start=start_date, end=end_date)
    # 格式化成交量和成交金額以小數點分隔
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
        stock_data = get_stock_data()
        response = "近一個月鴻海（2317.TW）股票歷史資料：\n" + stock_data.to_string()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
    elif re.match('告訴我秘密', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('才不告訴你哩！'))   
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
