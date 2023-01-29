import json
import time

import requests
from bs4 import BeautifulSoup

from eintf.common.helper import user_agent, convert_time
from eintf.db.db import get_collection


class ETF:
    skip_next = False

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
        articles_ = list(filter(lambda it: it, map(self.parse_article, article_list)))
        self.skip_next = False
        return articles_

    def parse_article(self, article):
        title_ = article.select_one("h1 a[href]")
        title = title_.text
        last_known_title = get_collection("news", {"filter": "etf"})[0]["title"]
        if title == last_known_title:
            self.skip_next = True
        if self.skip_next:
            return {}
        date = article.select_one("h4").text.strip()
        author = article.select_one("a[rel=author]").text
        url = title_.attrs["href"]
        return {
            "title": title,
            "date": convert_time(date, "%B %d, %Y"),
            "author": author,
            "url": url,
            "content": self.article(url).strip().replace("\n","")
        }
