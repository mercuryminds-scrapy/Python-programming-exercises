# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TripItem(Item):
    # define the fields for your item here like:
    # name = Field()
	bid = Field() 
	url = Field() 
	rating = Field() 
	rv_count = Field() 
	rv_date = Field() 
	rv_heading = Field()
	rv_rating = Field() 
	rv_dc = Field() 
	rv_profile = Field()
