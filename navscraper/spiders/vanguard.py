from datetime import date, datetime

from scrapy import log
from scrapy.http import FormRequest, Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

from navscraper.items import FundItem


class VanguardSpider(BaseSpider):
    """Vanguard.com ETF data scraper.
    """
    name = "vanguard"
    allowed_domains = ["vanguard.com"]

    # spider arguments
    fund_id = None
    date_start = None
    date_end = None

    date_format = '%m/%d/%Y'
    search_url = (
        'https://personal.vanguard.com/us/funds/tools/pricehistorysearch'
        '?FundId=null&FundType=ExchangeTradedShares'
    )

    def start_requests(self):
        if self.fund_id:
            yield Request(self.search_url, self.parse_form)
        else:
            self.log("Argument 'fund_id' missing.", level=log.ERROR)

    def parse_form(self, response):
        if not self.date_start:
            self.date_start = date.today().replace(month=1, day=1) \
                                  .strftime(self.date_format)
        if not self.date_end:
            self.date_end = date.today().strftime(self.date_format)

        meta = {
            'item': FundItem(fund_id=self.fund_id),
        }
        data = {
            'FundId': self.fund_id,
            'fundName': self.fund_id,
            'radiobutton2': '1',
            'radio': '1',
            'beginDate': self.date_start,
            'endDate': self.date_end,
            'results': 'get',
        }

        return FormRequest.from_response(response, formname='FormNavigate',
                                         formdata=data, meta=meta,
                                         callback=self.parse_results)

    def parse_results(self, response):
        hxs = HtmlXPathSelector(response)
        results = hxs.select(
            '//tr[count(th) = 2 and th[1][text()="Date"]]'
            '/following-sibling::tr/td/text()'
        ).extract()

        if results:
            results = iter(results)
            dates, values = zip(*zip(results, results))
            item = response.meta['item']
            item.update({
                'dates': map(self._parse_date, dates),
                'values': map(self._parse_value, values),
            })
            return item
        else:
            self.log("No results found {!r}".format(response), level=log.ERROR)

    def _parse_date(self, date_str):
        dt = datetime.strptime(date_str, self.date_format).date()
        return dt.isoformat()

    def _parse_value(self, value_str):
        # TODO: this is specific for vangard. Better to have a generic value
        # parser to handle other sites possible formats.
        return float(value_str.replace('$', ''))
