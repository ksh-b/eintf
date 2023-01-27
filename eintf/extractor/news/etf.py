import json
import time

import requests
from bs4 import BeautifulSoup

from eintf.common.helper import user_agent, convert_time


class ETF:

    def article(self, url):
        response = requests.get(url, headers=user_agent())
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.select_one(".post")
        html_content = str(body.select_one(".etf2l_page"))
        time.sleep(0.5)
        return html_content

    def articles(self):
        response = requests.get("https://etf2l.org", headers=user_agent())
        soup = BeautifulSoup(response.text, 'html.parser')
        article_list = soup.select(".post")
        return json.dumps(list(map(self.parse_article, article_list)))

    def parse_article(self, article):
        title_ = article.select_one("h1 a[href]")
        title = title_.text
        date = article.select_one("h4").text.strip()
        author = article.select_one("a[rel=author]").text
        url = title_.attrs["href"]
        return {
            "title": title,
            "date": convert_time(date, "%B %d, %Y"),
            "author": author,
            "url": url,
            "content": self.article(url)
        }

print(ETF().articles())