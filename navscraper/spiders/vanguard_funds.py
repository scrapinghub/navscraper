from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

from navscraper.items import FundLoader


class VanguardFundsSpider(BaseSpider):
    name = 'vanguard_funds'
    allowed_domains = ['vanguard.com']
    start_urls = ['https://personal.vanguard.com/us/funds/etf/all']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        rows = hxs.select(
            '//tbody[@id="tboxForm:upperTB:perfTB:avgAnnTBLtbody0"]'
            '/tr[count(./th)=0]'
        )
        for row in rows:
            fl = FundLoader(response=response, selector=row)
            fl.add_xpath('id', './td[2]/a/@href', re=r'FundId=(\d+)')
            fl.add_xpath('name', './td[2]/text()')
            fl.add_xpath('symbol', './td[3]/text()')
            yield fl.load_item()
