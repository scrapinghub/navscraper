from datetime import datetime

from scrapy import log
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

from navscraper.items import NavItem


class WisdomtreeSpider(BaseSpider):
    """WisdomTree.com ETF data scraper.

    Arguments
    ---------
    fund_id : str
        Fund's ID in WisdomTree website.
    """
    name = "wisdomtree"
    allowed_domains = ["wisdomtree.com"]

    fund_id = None

    date_format = '%m/%d/%Y'
    history_url = 'http://www.wisdomtree.com/etfs/nav-history.aspx?etfid=%(fund_id)s'

    def start_requests(self):
        if self.fund_id:
            # The site does not support query by start/end date as already
            # display all the history values.
            meta = {'fund_id': self.fund_id}
            url = self.history_url % meta
            yield Request(url, meta=meta, callback=self.parse_history)
        else:
            self.log("Argument 'fund_id' missing.", level=log.ERROR)

    def parse_history(self, response):
        fund_id = response.meta['fund_id']
        hxs = HtmlXPathSelector(response)
        results = hxs.select('//table[@title="NAV History"]'
                             '/tbody/tr/td/text()').extract()
        if results:
            results = iter(results)
            dates, values = zip(*zip(results, results))
            dates = map(self._parse_date, dates)
            values = map(float, values)
            # values are extracted in a reversed chronological order
            dates.reverse()
            values.reverse()

            return NavItem(fund_id=fund_id, dates=dates, values=values)
        else:
            self.log("No results found %r" % response, level=log.ERROR)

    # TODO: refactor this method
    def _parse_date(self, date_str):
        dt = datetime.strptime(date_str, self.date_format).date()
        return dt.isoformat()
