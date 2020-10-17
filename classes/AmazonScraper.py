from .logger import Logger
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re

logger = Logger("Amazon Scraper")


class AmazonScraper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding": "gzip, deflate",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Referer": "https://www.google.com/"}

    def getPrice(self, url: str) -> float:
        res = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(res.content, features="html.parser")
        priceTag = soup.find('span', attrs={'id': "priceblock_ourprice"}) or soup.find('span', attrs={'id': "priceblock_dealprice"}) 

        if(priceTag):
            content = priceTag.decode_contents()
            parts = re.findall("\d+", content)
            price = float(parts[0] + '.' + parts[1])
            return price
        else:
            logger.debug(soup)
            logger.error("No Price Found")
            return 0
