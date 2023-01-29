import re
import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

from eintf.common.helper import now
from eintf.db.db import update_collection


class MapsSpider(scrapy.Spider):
    name = "maps"

    latest = -1

    def start_requests(self):
        url = "https://tf2maps.net/sitemap-1.xml"
        xml_data = requests.get(url).content
        soup = BeautifulSoup(xml_data, "xml")
        urls = [loc.text for loc in soup.find_all('loc')]
        urls = list(filter(lambda link: "/downloads/" in str(link), urls))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_map)

    def parse_map(self, response):
        map_info = {
            'id': response.url.split("/")[-2],
            'name': response.css('.p-title-value::text').get(default='').strip(),
            'version': response.css('.p-title-value span::text').get(default='').strip(),
            'author': response.css('.resourceSidebarGroup a[class*=username] span::text').get(default='').strip(),
            'tagline': response.css('.p-tagline-value span::text').get(default='').strip(),
            'first-release': int(
                response.xpath("(//div[@class='resourceSidebarGroup']//time)[1]/@data-time").get(default='').strip()),
            'last-update': int(
                response.xpath("(//div[@class='resourceSidebarGroup']//time)[2]/@data-time").get(default='').strip()),
            'category': response.css(".resourceSidebarGroup a[href*='/categories/']::text").get(default='').strip(),
            'download-url': response.xpath(
                "//div[contains(@class,'resourceSidebarGroup')]//a[normalize-space()='Go to download']").attrib[
                'href'].strip(),
            'screens': list(map(lambda it: re.findall(r'\(.*?\)', it)[0].strip("(')"),
                                response.xpath("//div[@class='xfa_ec_img']/@style").getall())),
            'description': response.css('.bbWrapper').get(default=''),
        }

        print(map_info["id"])

        if map_info['last-update'] > self.latest:
            self.latest = map_info['last-update']

        update_collection(
            "maps",
            {"id": map_info["id"]},
            map_info,
            True
        )


# create a CrawlerProcess instance
process = CrawlerProcess()

# instantiate the spider and add it to the process
spider = MapsSpider
process.crawl(spider)

# start the crawling process
process.start()
