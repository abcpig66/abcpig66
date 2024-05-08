# -*- coding: utf-8 -*-
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import pandas as pd
import requests
import time
import json

app = Flask(__name__)

line_bot_api = LineBotApi('p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('980186763ec26279c6c95254f44a4ae8')

# 打算要取得的股票代碼
stock_list_tse = ['2330']
stock_list_otc = ['6180']
    
# 組合API需要的股票清單字串
stock_list1 = '|'.join('tse_{}.tw'.format(stock) for stock in stock_list_tse) 
stock_list2 = '|'.join('otc_{}.tw'.format(stock) for stock in stock_list_otc) 
stock_list = stock_list1 + '|' + stock_list2

# 組合完整的URL
query_url = f'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_list}'

# 呼叫股票資訊API
def get_stock_info():
    response = requests.get(query_url)
    if response.status_code != 200:
        raise Exception('取得股票資訊失敗.')
    else:
        data = json.loads(response.text)
        columns = ['c','n','z','tv','v','o','h','l','y', 'tlong']
        df = pd.DataFrame(data['msgArray'], columns=columns)
        df.columns = ['股票代號','公司簡稱','成交價','成交量','累積成交量','開盤價','最高價','最低價','昨收價', '資料更新時間']
        df.insert(9, "漲跌百分比", 0.0) 

        def count_per(x):
            if isinstance(x[0], int) == False:
                x[0] = 0.0
            result = (x[0] - float(x[1])) / float(x[1]) * 100
            return pd.Series(['-' if x[0] == 0.0 else x[0], x[1], '-' if result == -100 else result])

        df[['成交價', '昨收價', '漲跌百分比']] = df[['成交價', '昨收價', '漲跌百分比']].apply(count_per, axis=1)

        def time2str(t):
            t = int(t) / 1000 + 8 * 60 * 60. # UTC時間加8小時為台灣時間
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))

        df['資料更新時間'] = df['資料更新時間'].apply(time2str)
        return df

# 監聽所有來自 /webhook 的 Post Request
@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理收到的訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if message == '股票資訊':
        stock_info_df = get_stock_info()
        stock_info_text = stock_info_df.to_string(index=False)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=stock_info_text))

# 主程式
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
