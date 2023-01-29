import json
import time

import requests
from bs4 import BeautifulSoup

from eintf.common.helper import user_agent, convert_time
from eintf.db.db import get_collection


class UGC:
    skip_next = False

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
        time.sleep(0.5)
        return str(soup.select_one(".item"))

    def articles(self, game_format="highlander"):
        response = requests.get(
            f"https://www.ugcleague.com/home_{self.format_map[game_format]}_ALL.cfm",
            headers=user_agent()
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        article_list = soup.select(".item")[:10]
        articles_ = list(filter(lambda it: it, map(self.parse_article, article_list)))
        self.skip_next = False
        return articles_

    def parse_article(self, article):
        title = article.select_one(".item-title b").text
        last_known_title = get_collection("news", {"filter": "ugc"})[0]["title"]
        if title == last_known_title:
            self.skip_next = True
        if self.skip_next:
            return {}
        date_author = article.select_one("h6").text
        date = convert_time(date_author.split(" by ")[0].strip(), "%a, %b %d, %Y")
        author = date_author.split(" by ")[1].strip() if " by " in date_author else ""
        url = article.select_one("figure a").attrs["href"]
        url = f"https://www.ugcleague.com/{url}"
        return {
            "title": title,
            "date": date,
            "author": author,
            "url": url,
            "content": self.article(url).strip().replace("\n","")
        }

