import scrapy

from eintf.common.helper import convert_time, cleanse_html
from eintf.db.db import get_collection


class HatSpider(scrapy.Spider):
    name = "etf"

    start_urls = [
        "https://wiki.teamfortress.com/wiki/List_of_Scout_cosmetics",
        "https://wiki.teamfortress.com/wiki/List_of_Soldier_cosmetics",
        "https://wiki.teamfortress.com/wiki/List_of_Pyro_cosmetics",
        "https://wiki.teamfortress.com/wiki/List_of_Demoman_cosmetics",
        "https://wiki.teamfortress.com/wiki/List_of_Heavy_cosmetics",
        "https://wiki.teamfortress.com/wiki/List_of_Engineer_cosmetics",
        "https://wiki.teamfortress.com/wiki/List_of_Medic_cosmetics",
        "https://wiki.teamfortress.com/wiki/List_of_Sniper_cosmetics",
        "https://wiki.teamfortress.com/wiki/List_of_Spy_cosmetics",
        "https://wiki.teamfortress.com/wiki/List_of_All_class_cosmetics",
    ]

    def parse(self, response):
        urls = response.css("td[style*='1.25em'] a")
        for url in urls:
            if get_collection("hats").find_one({"url": url.get()}) is not None:
                break
            yield scrapy.Request(url=f"https://wiki.teamfortress.com/{url.get()}", callback=self.get_info)

    def get_info(self, response):
        url = response.url
        title = response.css("#firstHeading::text").get(default='').strip()
        descriptions = response.xpath("//*[@id='right-sidebar']//following-sibling::p[not(contains(., 'Patch'))]/text()")
        print(descriptions)


    def update(self, process):
        spider = HatSpider
        process.crawl(spider)

