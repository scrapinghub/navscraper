# Scrapy settings for navscraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'navscraper'

SPIDER_MODULES = ['navscraper.spiders']
NEWSPIDER_MODULE = 'navscraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'navscraper (+http://github.com/scrapinghub/navscraper)'
