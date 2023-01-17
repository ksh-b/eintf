import json

import requests
from bs4 import BeautifulSoup

from eintf.common.helper import user_agent


class RGL:

    def article(self, article_id):
        response = requests.get(f"https://rgl.gg/Public/Articles/Default.aspx?a={article_id}", headers=user_agent())
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.select_one("div[id*=divArticle]")
        title = body.select_one("span[id*=lblHeader]").text
        author = body.select_one("span[id*=lblWriterName]").text
        date = body.select_one("span[id*=lblDateLive]").text
        avatar = body.select_one("img[id*=imgWriterAvatar]").attrs["src"]
        html_content = str(body.select_one(".text-center+div[style]+div"))
        return json.dumps({"title": title, "author": author, "date": date, "avatar": avatar, "content": html_content})

    def articles(self):
        response = requests.get("https://rgl.gg/Public/Articles/ArticlesList.aspx", headers=user_agent())
        soup = BeautifulSoup(response.text, 'html.parser')
        article_list = soup.select(".table tr")
        return json.dumps(list(map(self.parse_article, article_list)))

    def parse_article(self, article):
        tds = article.select("td")
        title = tds[1].text.strip("\\r\\n").strip()
        date = tds[2].text.strip("\\r\\n").strip()
        url = tds[3].select_one("a").attrs["href"]
        return {"title": title, "date": date, "url": url}


print(RGL().articles())
