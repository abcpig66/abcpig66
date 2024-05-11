import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage

# 要搜尋的關鍵字
keyword = "台積電"

# 雅虎台灣新聞的搜尋鏈接
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
        news_list.append(f"標題： {news_title}\n連結： {news_link}\n")

# 將新聞列表轉換成文字訊息
news_message = "\n".join(news_list)

# 初始化 Line Bot API
line_bot_api = LineBotApi('p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=')

# 傳送新聞訊息給使用者
line_bot_api.push_message('980186763ec26279c6c95254f44a4ae8', TextSendMessage(text=news_message))
