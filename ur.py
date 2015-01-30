# _print " Enter Url here"
# url =['http://www.yelp.com/biz/firebrew-virginia-beach','http://www.yelp.com/biz/taboon-grand-blanc-grand-blanc-township','http://www.yelp.com/biz/lincoln-washington','http://www.yelp.com/biz/zingermans-delicatessen-ann-arbor-2']
# url =['http://www.urbanspoon.com/r/1/4524/restaurant/Capitol-Hill/Honey-Hole-Sandwiches-Seattle','http://www.urbanspoon.com/r/1/4524/restaurant/Capitol-Hill/Honey-Hole-Sandwiches-Seattle','http://www.urbanspoon.com/r/13/169913/restaurant/North-Richland-Hills-Richland-Hills/Texs-Star-Grill-Watauga']
#
# from scrapy.spider import BaseSpider
# from scrapy.http import Request
# from urlparse import urljoin
# from scrapy.selector import HtmlXPathSelector
# from urbans.items import UrbansItem
import psycopg2
# import time
#
#
# """ Database Creation"""
import datetime
con = psycopg2.connect(database="mm", user="postgres", password="mercuryminds", host="localhost")
cur = con.cursor()
bid=12
cur.execute("select max(d) from y where id='%s'" %bid)
r = cur.fetchall()
i = r[0][0]
x='2015-01-25'

try:
	ff = datetime.datetime.strptime(x, '%Y-%m-%d')
except:
    ff = datetime.datetime.strptime('1', '%d')
try:
	if ff >= i:
		print "ok"
	else:
		print i,ff
except:
	print "do "
#print r,'\n',type(i),i,len(i)
#
# class UrbansSpider(BaseSpider):
#
#
# 	name = "urban"
# 	start_urls=[url[i] for i in range(len(url))]
# 	f=open('opt.csv','w')
#
# 	def parse(self, response):
#
# 		itm=[]
# 		hxs = HtmlXPathSelector(response)
# 		item = UrbansItem()
#
# 		item['bid'] = 1
# 		item['u'] = response.url
# 		item['li'] = hxs.select('//div[@class="rating"]/text()').extract()[0].encode('utf-8')
# 		item['nv'] = hxs.select('//div[@class="stats"]/div/text()').extract()[0].encode('utf-8').replace('\n','')
# 		item['nr'] = hxs.select('//a[@data-ga-action="reviews"]/text()').extract()[0].encode('utf-8').split(' ')[0]
# 		x= 'http://www.urbanspoon.com'+hxs.select('//div[@data-ga-action="diner-reviews"]/@data-url').extract()[0].encode('utf-8')
# 		if x:
# 			yield Request(x, callback=self.parse_sub, meta={'item':item})
#
# 	def parse_sub(self, response):
#
# 		item = UrbansItem(response.meta['item'])
#
# 		hxs = HtmlXPathSelector(response)
#
# 		for i in range(20):
# 			o=hxs.select('//div[@class="title"]/text()').extract()[i].encode('utf-8').replace("'","")
# 			u= hxs.select('//a[@data-ga-action="user-profile-page"]/text()').extract()[i].encode('utf-8')
# 			e=hxs.select('//time[@class="posted-on"]/text()').extract()[i].encode('utf-8').split(' ')[2].replace('\n','')
# 			e1=time.strftime(e)
# 			print type(e1)
#
# 			item['rd'] =  hxs.select('//div[@itemprop="description"]/text()').extract()[i].encode('utf-8').replace('\n','').replace("'","").strip()
# 			sql = ("insert into public.ep select %s,'%s','%s',%s,%s,'%s','%s','%s','%s' where not exists ( select * from public.ep where dc='%s' and us='%s')"%(item['bid'],item['u'],item['nv'],item['li'],item['nr'],e1,o,item['rd'],u,item['rd'],u))
# 			cur.execute(sql)
#                 	con.commit()
#
#
#
#
#
#
# <html>
# <head>
# <title> Sprites </title>
# <style>
#
# .rating-image {
# background: url(https://s3-media4.fl.yelpcdn.com/assets/srv0/yelp_styleguide/c2252a4cd43e/assets/img/stars/stars_map.png) no-repeat;
# float: left;
# width: 128px;
# height: 22px;
# }
# #star_4
# {
# background-position: -3px -689px;
# }
# #star_4_half
# {
# background-position: -3px -714px;
# }
# #star_5
# {
# background-position: -3px -739px;
# }
# </style>
# </head>
# <body>
#
# <div class="rating-image" id="star_4">
#
#     </div>
# <div class="rating-image" id="star_4_half">
#
#     </div>
# <div class="rating-image" id="star_5">
#
#     </div>
# </body>
# </html>
#
#
#
#
#
#
#
# " Enter Url here"
#
# url =['http://www.yelp.com/biz/firebrew-virginia-beach','http://www.yelp.com/biz/sabra-design-washington-3?osq=web+design+companies']
#
# from scrapy.spider import BaseSpider
# from scrapy.http import Request
# from urlparse import urljoin
# from scrapy.selector import HtmlXPathSelector
# from urbans.items import UrbansItem
# import psycopg2
# import time
#
#
# """ Database Creation"""
# con = psycopg2.connect(database="mm", user="postgres", password="mercuryminds", host="localhost")
# cur = con.cursor()
# cur.close()
# class UrbansSpider(BaseSpider):
#
#
# 	name = "ylp"
# 	start_urls=[url[i] for i in range(len(url))]
# 	f=open('opt.csv','w')
# 	count = 0
# 	def parse(self, response):
#
# 		itm=[]
# 		hxs = HtmlXPathSelector(response)
# 		item = UrbansItem()
# 		item['bid'] = 0
# 		item['url'] = response.url
# 		qu = ("select distinct u from ssdd")
# 		cur.execute(qu)
# 		rows = cur.fetchall()
# 		li = [r[0] for r in rows]
# 		print li
# 		for i in range(len(li)):
# 			print li[i], item['url']
# 			if li[i] in item['url']:
# 				qu1 = ("select distinct id from ssdd where u='%s'")%li[i]
# 				cur.execute(qu1)
# 				cur
# 				rows1= cur.fetchall()
# 				li1=[i[0] for i in rows1]
# 				print li1
# 				if len(li1) > 0:
# 					item['bid'] = li1[0]
# 		if item['bid'] > 0:
# 			print " ID assigned"
# 		else:
# 			item['bid'] = input("Enter the Business Id here")
#
#
# 		print item['bid']
# 		item['rating'] = float(hxs.select('//div[@itemprop="aggregateRating"]/div/meta/@content').extract()[0].encode('utf-8').strip())
# 		item['rv_count'] = int(hxs.select('//span[@itemprop="reviewCount"]/text()').extract()[0].encode('utf-8').strip())
#
# 		if item['rv_count'] > 0:
#
# 			no = len(hxs.select('//div[@itemprop="review"]').extract())
# 			x=hxs.select('//div[@class="review-list"]/ul/li')
# 			for i in range(no):
#
# 				self.__class__.count  = self.__class__.count + 1
# 				try:
# 					item['rv_date'] = x[0].select('//meta[@itemprop="datePublished"]/@content').extract()[i].encode('utf-8').strip()
# 				except:
# 					item['rv_date'] = 'NULL'
# 				try:
# 					item['rv_profile'] = x[0].select('//li[@class="user-name"]/a/text()').extract()[i].encode('utf-8').strip()
# 				except:
# 					item['rv_profile'] = 'NULL'
# 				try:
# 					item['rv_rating'] =  float(x[0].select('//div[@itemprop="reviewRating"]/div/meta/@content').extract()[i].encode('utf-8').strip())
# 				except:
# 					item['rv_rating'] = 'NULL'
# 				try:
# 					item['rv_dc'] = x[0].select('//div[@class="review-content"]/p').extract()[i].encode('utf-8').split('lang="en">')[1].replace("<br>",'').replace('</p>','').replace('\xc2','').replace('\xa0','').replace("'"," ").strip()
# 				except:
# 					item['rv_dc'] = 'NULL'
#
# 				sql = ("insert into public.ssdd select %s,'%s',%s,%s,'%s','%s','%s',%s where not exists ( select * from public.ssdd where dc='%s' and p='%s')"%(item['bid'],item['url'],item['rating'],item['rv_count'],item['rv_date'],item['rv_profile'],item['rv_dc'],item['rv_rating'],item['rv_dc'],item['rv_profile']))
#
# 				cur.execute(sql)
# 	                	con.commit()
#
# 			print self.__class__.count
# 			if item['rv_count'] > self.__class__.count:
#
# 				nxt_link = hxs.select('//a[@class="page-option prev-next"]/@href').extract()[0].encode('utf-8').strip()
#
# 				if nxt_link:
# 					""" Next link Processed """
# 					yield Request( nxt_link, callback=self.parse)
#
# 			else:
# 				self.__class__.count  = 0
# 				""" Reviews below 40 for this business"""
#
# 		else:
# 			item['rv_date'] = 'NULL'
# 			item['rv_profile'] = 'NULL'
# 			item['rv_rating'] = 'NULL'
# 			item['rv_dc'] = 'NULL'
#
#
#
#
#
