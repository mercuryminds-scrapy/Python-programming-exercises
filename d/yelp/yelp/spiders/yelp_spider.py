" Enter Url here"

url =['http://www.yelp.com/biz/firebrew-virginia-beach','http://www.yelp.com/biz/taboon-grand-blanc-grand-blanc-township','http://www.yelp.com/biz/lincoln-washington','http://www.yelp.com/biz/zingermans-delicatessen-ann-arbor-2']
#url =['http://www.yelp.com/biz/firebrew-virginia-beach']

from scrapy.spider import BaseSpider
from scrapy.http import Request
from urlparse import urljoin
from scrapy.selector import HtmlXPathSelector
from yelp.items import YelpItem
import psycopg2



""" Database Creation"""
try:
	con = psycopg2.connect(database="mm", user="postgres", password="mercuryminds", host="localhost")
	cur = con.cursor()
except:
	""" Database not Connected """

class YelpSpider(BaseSpider):
	

	name = "ylpp"
	start_urls=[url[i] for i in range(len(url))]
#	f=open('opt.csv','w')
	count = 0
	def parse(self, response):
		
		itm=[]
		hxs = HtmlXPathSelector(response)
		item = YelpItem()	 
		item['bid'] = 0
		item['url'] = response.url

		"""Getting the Business Id from the DB if exists """

		qu = ("select distinct url from social_data.yelp")
		cur.execute(qu)
		rows = cur.fetchall()
		li = [r[0] for r in rows]
#		print li
		for i in range(len(li)):
	#		print li[i], item['url']
			if li[i] in item['url']:
				qu1 = ("select distinct bid from social_data.yelp where url='%s'")%li[i]
				cur.execute(qu1)
				rows1= cur.fetchall()
				li1=[i[0] for i in rows1]
	#			print li1				
				if len(li1) > 0:
					item['bid'] = li1[0]
		if item['bid'] > 0:
			print " ID assigned"
		else:
			item['bid'] = input("Enter the Business Id here for URL:       %s        : "%item['url'])

		print item['bid']




		item['rating'] = float(hxs.select('//div[@itemprop="aggregateRating"]/div/meta/@content').extract()[0].encode('ascii', 'ignore').strip())
		item['rv_count'] = int(hxs.select('//span[@itemprop="reviewCount"]/text()').extract()[0].encode('ascii', 'ignore').strip())
	
		if item['rv_count'] > 0:

			no = len(hxs.select('//div[@itemprop="review"]').extract())
			x=hxs.select('//div[@class="review-list"]/ul/li')
			for i in range(no):

				self.__class__.count  = self.__class__.count + 1
				try:
					item['rv_date'] = x[0].select('//meta[@itemprop="datePublished"]/@content').extract()[i].encode('ascii', 'ignore').strip()
				except:
					item['rv_date'] = 'NULL'
				try:
					item['rv_profile'] = x[0].select('//li[@class="user-name"]/a/text()').extract()[i].encode('ascii', 'ignore').replace('.','').replace("'","").strip()
				except:
					item['rv_profile'] = 'NULL'
				try:
					item['rv_rating'] =  float(x[0].select('//div[@itemprop="reviewRating"]/div/meta/@content').extract()[i].encode('ascii', 'ignore').strip())
				except:
					item['rv_rating'] = 'NULL'
				try:
					item['rv_dc'] = x[0].select('//div[@class="review-content"]/p').extract()[i].encode('ascii', 'ignore').split('lang="en">')[1].replace("<br>",'').replace('</p>','').replace("'"," ").replace('.','').strip()
				except:					
					item['rv_dc'] = 'NULL'

				
			#	sql = ("insert into social_data.yelp select '%s','%s','%s,'%s','%s','%s','%s','%s' where not exists ( select * from social_data.yelp where rv_desc='%s' and rv_user='%s')"%(item['bid'],item['url'],item['rating'],item['rv_count'],item['rv_date'],item['rv_rating'],item['rv_dc'],item['rv_profile'],item['rv_dc'],item['rv_profile']))

				sql = ("insert into social_data.yelp select '%s','%s','%s','%s','%s','%s','%s','%s' where not exists ( select * from social_data.yelp where rv_desc='%s' and rv_user='%s')"%(item['bid'],item['url'],item['rating'],item['rv_count'],item['rv_date'],item['rv_rating'],item['rv_dc'],item['rv_profile'],item['rv_dc'],item['rv_profile']))

				cur.execute(sql)
	                	con.commit()
				print item['url'],item['rv_profile']
			print self.__class__.count
#			if item['rv_count'] > self.__class__.count:

			"""Check the review which has more than 40"""
			if item['rv_count'] > 40:				
#				nxt_link = hxs.select('//a[@class="page-option prev-next"]/@href').extract()[0].encode('ascii', 'ignore').split('?')[0]+'?start=%s'%self.__class__.count
				nxt_link = []

				""" Parse the nex review link by multiple of 40"""


				if float(item['rv_count'])/40 > item['rv_count']/40:
					x= range(40,(item['rv_count']/40)*40+1,40)
					for i in range(len(x)):
						nxt_link.append(hxs.select('//a[@class="page-option prev-next"]/@href').extract()[0].encode('ascii', 'ignore').split('?')[0]+'?start=%s'%x[i])
				else:					
					x= range(40,(item['rv_count']/40-1)*40+1,40)
					for i in range(len(x)):
						nxt_link.append(hxs.select('//a[@class="page-option prev-next"]/@href').extract()[0].encode('ascii', 'ignore').split('?')[0]+'?start=%s'%x[i])
				print nxt_link
				for i in range(len(nxt_link)):
					if nxt_link[i]:
						""" Next link Processed """
						yield Request( nxt_link[i], callback=self.parse)
				
			else:

				self.__class__.count  = 0

				""" Reviews below 40 for this business"""
				
		else:
			item['rv_date'] = 'NULL'
			item['rv_profile'] = 'NULL'
			item['rv_rating'] = 'NULL'
			item['rv_dc'] = 'NULL'




