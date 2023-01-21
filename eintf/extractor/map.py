import json

import requests
from bs4 import BeautifulSoup

from eintf.common.helper import user_agent


class Map:
    __featured_url = "https://tf2maps.net/downloads/featured"
    __downloads_url = "https://tf2maps.net/downloads/{}/?page={}&{}"
    __categories_url = "https://tf2maps.net/downloads/categories/{}/?page={}&{}"

    def downloads(self, page=1, extras=""):
        return self.__extract_featured(str.format(self.__categories_url, page, extras))

    def featured_downloads(self):
        return self.__extract_featured(self.__featured_url)

    def category(self, category, page=1, extras=""):
        return self.__extract_featured(str.format(self.__categories_url, category, page, extras))

    def __extract_featured(self, url):
        extract_dict = {}
        response = requests.get(url, headers=user_agent())
        soup = BeautifulSoup(response.text, 'html.parser')
        map_items = soup.select(".structItem--resource")
        for map_item in map_items:
            map_info = self.__map_info(map_item)
            extract_dict[map_info[0]] = map_info[1]
        return json.dumps(extract_dict, indent=4)

    def __map_info(self, map_item):
        try:
            thumbnail = map_item.select(".avatar--s")[0].find("img").get("src")
        except:
            thumbnail = ""
        title = map_item.select(".structItem-title")[0].text
        name = title.split('\n')[1]
        version = title.split('\n')[2]
        url = map_item.select(".structItem-title")[0].a["href"]
        username = map_item.select("span[class*=username]")[0].text
        start_date = map_item.select(".structItem-startDate")[0].text
        try:
            category = map_item.select(".structItem-startDate+li")[0].text
        except:
            category = ""
        tag_line = map_item.select(".structItem-resourceTagLine")[0].text
        updated_date = map_item.select(".u-concealed")[0].text
        downloads = map_item.select(".structItem-metaItem--downloads dd")[0].text
        return url.split("/")[2].split(".")[0], {
            "name": name,
            "version": version,
            "tag-line": tag_line,
            "url": url,
            "thumbnail": thumbnail,
            "username": username,
            "category": category,
            "start-date": start_date,
            "updated-date": updated_date,
            "downloads": downloads,
        }

