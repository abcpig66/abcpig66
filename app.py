# 匯入所需套件
import requests
from bs4 import BeautifulSoup

# 設定搜尋關鍵字
keyword = "台積電"

# 定義函式以擷取新聞標題和連結
def fetch_news(keyword):
    # 製作雅虎台灣新聞的搜尋 URL
    search_url = f"https://tw.news.yahoo.com/search?p={keyword}"

    # 發送 GET 請求
    response = requests.get(search_url)

    # 使用 BeautifulSoup 解析 HTML 內容
    soup = BeautifulSoup(response.content, "html.parser")

    # 找到所有的新聞標題和連結
    news_results = soup.find_all('h3')

    # 提取新聞標題和連結
    news_list = []
    for result in news_results:
        link_tag = result.find('a', href=True)
        if link_tag:
            news_title = link_tag.text
            news_link = link_tag['href']
            news_list.append((news_title, news_link))

    return news_list

# 設定 Line Bot 回應訊息的處理程序
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match('關鍵字', message):
        news_list = fetch_news("台積電")
        news_response = "\n".join([f"{title}: {link}" for title, link in news_list])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(news_response))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
