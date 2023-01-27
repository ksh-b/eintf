import json
import time

import requests
from bs4 import BeautifulSoup

from eintf.common.helper import user_agent, convert_time


class RGL:

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
        return json.dumps(list(map(self.parse_article, article_list)))

    def parse_article(self, article):
        tds = article.select("td")
        title = tds[1].text.strip("\\r\\n").strip()
        date = tds[2].text.strip("\\r\\n").strip()
        url = tds[3].select_one("a").attrs["href"]
        article_ = self.article(url)
        return {
            "title": title,
            "date": convert_time(date, "%m/%d/%Y"),
            "author": article_["author"],
            "url": f"https://rgl.gg/Public/Articles/{url}",
            "content": article_["content"]
        }


