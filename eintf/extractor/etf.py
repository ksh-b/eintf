import json

import requests
from bs4 import BeautifulSoup

from eintf.common.helper import user_agent


class ETF:

    def article(self, url):
        response = requests.get(url, headers=user_agent())
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.select_one(".post")
        title = body.select_one("h1 a").text
        author = body.select_one("a[rel=author]").text
        date = body.select_one("h4").text
        avatar = ""
        html_content = str(body.select_one(".etf2l_page"))
        return json.dumps({"title": title, "author": author, "date": date, "avatar": avatar, "content": html_content})

    def articles(self):
        response = requests.get("https://etf2l.org", headers=user_agent())
        soup = BeautifulSoup(response.text, 'html.parser')
        article_list = soup.select(".post")
        return json.dumps(list(map(self.parse_article, article_list)))

    def parse_article(self, article):
        title_ = article.select_one("h1 a[href]")
        title = title_.text
        date = article.select_one("h4").text
        author = article.select_one("a[rel=author]").text
        url = title_.attrs["href"]
        return {"title": title, "date": date, "url": url, "author": author}