__author__ = 'anandhakumar'


print " Enter Url here"

url ='http://www.urbanspoon.com/r/1/4524/restaurant/Capitol-Hill/Honey-Hole-Sandwiches-Seattle'

from scrapy.spider import BaseSpider
from scrapy.http import Request
from urlparse import urljoin
from scrapy.selector import HtmlXPathSelector
from urbans.items import UrbansItem
import psycopg2


""" Database Creation"""
con = psycopg2.connect(database="mm", user="postgres", password="mercuryminds", host="localhost")
cur = con.cursor()

class UrbansSpider(BaseSpider):


	name = "urban"
	start_urls=['%s'%url]
	f=open('opt.csv','w')

	def parse(self, response):

		itm=[]
		hxs = HtmlXPathSelector(response)
		item = UrbansItem()

		item['bid'] = 1
		item['u'] = response.url
		item['li'] = hxs.select('//div[@class="rating"]/text()').extract()[0].encode('utf-8')
		item['nv'] = hxs.select('//div[@class="stats"]/div/text()').extract()[0].encode('utf-8').split(' ')[0].replace('\n','')
		item['nr'] = hxs.select('//a[@data-ga-action="reviews"]/text()').extract()[0].encode('utf-8').split(' ')[0]
		x= 'http://www.urbanspoon.com'+hxs.select('//div[@data-ga-action="diner-reviews"]/@data-url').extract()[0].encode('utf-8')
		if x:
			yield Request(x, callback=self.parse_sub, meta={'item':item})

	def parse_sub(self, response):
        item = UrbansItem(response.meta['item'])
    	hxs = HtmlXPathSelector(response)

		for i in range(40):

			item['rd'] =  hxs.select('//div[@itemprop="description"]/text()').extract()[i].encode('utf-8').replace('\n','').replace("'","").strip()
			sql = ("insert into public.ub values(%s,'%s',%s,%s,%s,'%s') except select * from public.ub"%(item['bid'],item['u'],item['li'],item['nv'],item['nr'],item['rd']))
			cur.execute(sql)
                	con.commit()



		#	self.f.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(item['bid'],item['u'],item['li'],item['nv'],item['nr'],item['rd']))

