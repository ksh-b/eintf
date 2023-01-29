import json
import time

import requests
from bs4 import BeautifulSoup

from eintf.common.helper import user_agent, convert_time
from eintf.db.db import get_collection


class RGL:

    skip_next = False

    def article(self, url):
        response = requests.get(f"https://rgl.gg/Public/Articles/{url}", headers=user_agent())
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.select_one("div[id*=divArticle]")
        author = body.select_one("span[id*=lblWriterName]").text
        html_content = str(body.select_one(".text-center+div[style]+div"))
        time.sleep(0.5)
        return {"author": author, "content": html_content}

    def articles(self):
        response = requests.get("https://rgl.gg/Public/Articles/ArticlesList.aspx", headers=user_agent())
        soup = BeautifulSoup(response.text, 'html.parser')
        article_list = soup.select(".table tr")[:10]
        articles_ = list(filter(lambda it: it, map(self.parse_article, article_list)))
        self.skip_next = False
        return articles_

    def parse_article(self, article):
        tds = article.select("td")
        title = tds[1].text.strip("\\r\\n").strip()
        date = tds[2].text.strip("\\r\\n").strip()
        last_known_title = get_collection("news", {"filter": "rgl"})[0]["title"]
        if title == last_known_title:
            self.skip_next = True
        if self.skip_next:
            return {}
        url = tds[3].select_one("a").attrs["href"]
        article_ = self.article(url)
        return {
            "title": title,
            "date": convert_time(date, "%m/%d/%Y"),
            "author": article_["author"],
            "url": f"https://rgl.gg/Public/Articles/{url}",
            "content": article_["content"].strip().replace("\n", "")
        }
