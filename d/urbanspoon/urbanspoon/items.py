# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class UrbanspoonItem(Item):
    # define the fields for your item here like:
    # name = Field()
    b_id = Field()
    url = Field()
    n_votes = Field()
    p_like= Field()
    n_reviews= Field()
    date= Field()
    title= Field()
    description= Field()
    user = Field()



