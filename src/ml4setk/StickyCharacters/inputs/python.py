# 你需要先安装 requests 和 beautifulsoup4 库:
# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
import time

def scrape_headlines(url):
    """
    爬取指定 URL 的所有 h2 标题
    """
    print(f"正在爬取: {url}\n")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # 发送 HTTP GET 请求
        response = requests.get(url, headers=headers, timeout=10)
        # 如果响应状态码不是 200，则引发异常
        response.raise_for_status()

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有的 <h2> 标签
        headlines = soup.find_all('h2')

        if not headlines:
            print("没有找到 <h2> 标题。")
            return

        print("--- 找到的标题 ---")
        for index, headline in enumerate(headlines, 1):
            # 清理文本并打印
            print(f"{index}. {headline.get_text(strip=True)}")
        print("------------------\n")

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")


# 示例：爬取一个新闻网站的标题
if __name__ == "__main__":
    # 使用一个有 h2 标签的示例网站
    scrape_headlines('http://pyclass.com/real-estate')