from bs4 import BeautifulSoup
import requests
import re

from creepycrawly.database.model import Stock





# http://www.finanzen.at/suchergebnisse?_search=AT0000831706



class FinanzenNetCrawler:
    def _open_price(self, html):
        price = html.select('div.pricebox.content_box > div.content > table:nth-of-type(2) '
                            '> tr:nth-of-type(2) > td:nth-of-type(4)')[0].text

        return float(re.sub(',', '.', price))

    def _volume(self, html):
        volStr = html.select('div.pricebox.content_box > div.content '
                             '> table:nth-of-type(2) > tr:nth-of-type(4) '
                             '> td:nth-of-type(4)')[0].text
        return int(re.sub('\.', '', volStr))

    def parse(self, html):
        '''
        starts the actual crawling of the page and extracts its data
        :param isin: the international securities identification number
        :return:
        '''

        vol = self._volume(html)
        price = self._open_price(html)

        return (vol, price)



def crawl(isin):
    resp = requests.get("http://www.finanzen.at/suchergebnisse?_search=" + isin,
                    headers={"content-type": "text",
                             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 "
                                           "(KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"})
    return resp.text



# print(resp.text)
crawler = FinanzenNetCrawler()
isin = "AT0000831706"
print("Volume of %s: %s" % (isin, crawler.parse(BeautifulSoup(crawl(isin), 'html.parser'))))
isin = "DE0007164600"
print("Volume of %s: %s" % (isin, crawler.parse(BeautifulSoup(crawl(isin), 'html.parser'))))
isin = "DE0007037129"
print("Volume of %s: %s" % (isin, crawler.parse(BeautifulSoup(crawl(isin), 'html.parser'))))
