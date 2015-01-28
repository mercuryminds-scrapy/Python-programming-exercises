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
		item['nv'] = hxs.select('//div[@class="stats"]/div/text()').extract()[0].encode('utf-8').replace('\n','')
		item['nr'] = hxs.select('//a[@data-ga-action="reviews"]/text()').extract()[0].encode('utf-8').split(' ')[0]
		x= 'http://www.urbanspoon.com'+hxs.select('//div[@data-ga-action="diner-reviews"]/@data-url').extract()[0].encode('utf-8')
		if x:
			yield Request(x, callback=self.parse_sub, meta={'item':item})

	def parse_sub(self, response):

		item = UrbansItem(response.meta['item'])

		hxs = HtmlXPathSelector(response)

		for i in range(20):
			o=hxs.select('//div[@class="title"]/text()').extract()[i].encode('utf-8')
			u= hxs.select('//a[@data-ga-action="user-profile-page"]/text()').extract()[i].encode('utf-8')
			e=hxs.select('//time[@class="posted-on"]/text()').extract()[i].encode('utf-8').split(' ')[2].replace('\n','')
			e1=time.strftime(e)
			print type(e1)

			item['rd'] =  hxs.select('//div[@itemprop="description"]/text()').extract()[i].encode('utf-8').replace('\n','').replace("'","").strip()
			sql = ("insert into public.ep select %s,'%s','%s',%s,%s,'%s','%s','%s','%s' where not exists ( select * from public.ep where dc='%s' and us='%s')"%(item['bid'],item['u'],item['nv'],item['li'],item['nr'],e1,o,item['rd'],u,item['rd'],u))
			cur.execute(sql)
            con.commit()




<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>CSS sprites</title>
    <style>

.rating-image {
display: block;
background: url(https://s3-media4.fl.yelpcdn.com/assets/srv0/yelp_styleguide/c2252a4cd43e/assets/img/stars/stars_map.png) no-repeat;
float: left;
overflow: hidden;
position: relative;
width: 128px;
height: 22px;
}
#star_4
{
background-position: -3px -689px;
}
#star_4_half
{
background-position: -3px -714px;
}
#star_5
{
background-position: -3px -739px;
}
</style>
</head>
<body>

<div class="rating-image" id="star_4">

    </div><br><br>
<div class="rating-image" id="star_4_half">

    </div><br><br>
<div class="rating-image" id="star_5">

    </div>
</body>
</html>