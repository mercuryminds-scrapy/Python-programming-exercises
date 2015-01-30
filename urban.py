" Enter Url here"

url =['http://www.yelp.com/biz/firebrew-virginia-beach','http://www.yelp.com/biz/sabra-design-washington-3?osq=web+design+companies']


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
	

	name = "ylp"
	start_urls=[url[i] for i in range(len(url))]
	f=open('opt.csv','w')
	count = 0
	def parse(self, response):
		
		itm=[]
		hxs = HtmlXPathSelector(response)
		item = UrbansItem()	 
		item['bid'] = 0
		item['url'] = response.url
		qu = ("select distinct u from ssdd")
		cur.execute(qu)
		rows = cur.fetchall()
		li = [r[0] for r in rows]
		print li
		for i in range(len(li)):
			print li[i], item['url']
			if li[i] in item['url']:
				qu1 = ("select distinct id from ssdd where u='%s'")%li[i]
				cur.execute(qu1)
				rows1= cur.fetchall()
				li1=[i[0] for i in rows1]
				print li1				
				if len(li1) > 0:
					item['bid'] = li1[0]
		if item['bid'] > 0:
			print " ID assigned"
		else:
			item['bid'] = input("Enter the Business Id here")


		print item['bid']
		item['rating'] = float(hxs.select('//div[@itemprop="aggregateRating"]/div/meta/@content').extract()[0].encode('utf-8').strip())
		item['rv_count'] = int(hxs.select('//span[@itemprop="reviewCount"]/text()').extract()[0].encode('utf-8').strip())
	
		if item['rv_count'] > 0:

			no = len(hxs.select('//div[@itemprop="review"]').extract())
			x=hxs.select('//div[@class="review-list"]/ul/li')
			for i in range(no):

				self.__class__.count  = self.__class__.count + 1
				try:
					item['rv_date'] = x[0].select('//meta[@itemprop="datePublished"]/@content').extract()[i].encode('utf-8').strip()
				except:
					item['rv_date'] = 'NULL'
				try:
					item['rv_profile'] = x[0].select('//li[@class="user-name"]/a/text()').extract()[i].encode('utf-8').strip()
				except:
					item['rv_profile'] = 'NULL'
				try:
					item['rv_rating'] =  float(x[0].select('//div[@itemprop="reviewRating"]/div/meta/@content').extract()[i].encode('utf-8').strip())
				except:
					item['rv_rating'] = 'NULL'
				try:
					item['rv_dc'] = x[0].select('//div[@class="review-content"]/p').extract()[i].encode('utf-8').split('lang="en">')[1].replace("<br>",'').replace('</p>','').replace('\xc2','').replace('\xa0','').replace("'"," ").strip()
				except:					
					item['rv_dc'] = 'NULL'
			
				sql = ("insert into public.ssdd select %s,'%s',%s,%s,'%s','%s','%s',%s where not exists ( select * from public.ssdd where dc='%s' and p='%s')"%(item['bid'],item['url'],item['rating'],item['rv_count'],item['rv_date'],item['rv_profile'],item['rv_dc'],item['rv_rating'],item['rv_dc'],item['rv_profile']))

				cur.execute(sql)
	                	con.commit()

			print self.__class__.count
			if item['rv_count'] > self.__class__.count:
				
				nxt_link = hxs.select('//a[@class="page-option prev-next"]/@href').extract()[0].encode('utf-8').strip()
				
				if nxt_link:
					""" Next link Processed """
					yield Request( nxt_link, callback=self.parse)
				
			else:
				self.__class__.count  = 0
				""" Reviews below 40 for this business"""
				
		else:
			item['rv_date'] = 'NULL'
			item['rv_profile'] = 'NULL'
			item['rv_rating'] = 'NULL'
			item['rv_dc'] = 'NULL'




