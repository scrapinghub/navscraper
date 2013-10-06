# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class FundItem(Item):
    fund = Field()
    fund_id = Field()
    dates = Field()
    values = Field()
