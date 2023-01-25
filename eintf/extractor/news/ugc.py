import json

import requests
from bs4 import BeautifulSoup

from eintf.common.helper import user_agent


class UGC:
    format_map = {
        "highlander": "tf2h",
        "6v6": "tf26",
        "4v4": "tf24",
        "ultiduo": "tf22",
        "asia-highlander": "atf2h",
        "asia-6v6": "atf26",
    }

    def article(self, url):
        response = requests.get(url, headers=user_agent())
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.select_one(".item")
        title = body.select_one(".item .item-title").text.strip()
        date_author = body.select_one("h5").text.strip()
        date = date_author.split("by")[0].strip()
        author = date_author.split("by")[1].strip() if "by" in date_author else ""
        html_content = str(body)
        return json.dumps({"title": title, "author": author, "date": date, "avatar": "", "content": html_content})

    def articles(self, game_format="highlander"):
        response = requests.get(
            f"https://www.ugcleague.com/home_{self.format_map[game_format]}_ALL.cfm",
            headers=user_agent()
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        article_list = soup.select(".item")
        return json.dumps(list(map(self.parse_article, article_list)))

    def parse_article(self, article):
        title = article.select_one(".item-title b").text
        date_author = article.select_one("h6").text
        date = date_author.split(" by ")[0].strip()
        author = date_author.split(" by ")[1].strip() if " by " in date_author else ""
        url = article.select_one("figure a").attrs["href"]
        return {"title": title, "date": date, "url": url, "author": author}
