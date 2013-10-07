import json

from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

from navscraper.items import FundItem


class WisdomtreeFundsSpider(BaseSpider):
    name = 'wisdomtree_funds'
    allowed_domains = ['wisdomtree.com']
    start_urls = ['http://www.wisdomtree.com/etfs/']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        try:
            jsdata = hxs.select('//script[contains(.,"var results")]') \
                        .re('var results = (.+?);')[0]
        except IndexError:
            self.log('JS funds data not found %r' % response, level=log.ERROR)
            return

        try:
            data = json.loads(jsdata)['data']
        except ValueError:
            self.log('Could not load JS data %r' % jsdata, level=log.ERROR)
        except KeyError:
            self.log('Could not find data field %r' % jsdata, level=log.ERROR)

        for etf in data:
            yield FundItem(
                id=etf['ETFID'],
                name=etf['fund'],
                symbol=etf['ticker'],
            )
