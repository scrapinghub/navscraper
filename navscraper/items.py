# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.item import Item, Field


class FundItem(Item):
    id = Field()
    name = Field()
    symbol = Field()


class NavItem(Item):
    fund_id = Field()
    dates = Field()
    values = Field()


class FundLoader(XPathItemLoader):
    default_item_class = FundItem
    default_output_processor = TakeFirst()
