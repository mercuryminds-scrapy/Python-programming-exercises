" Enter Url here"

""" Before enter the URL please check when the sort by date is performed the url is appends only the date params """

""" If not please edit the url and enter in below list"""


url =['http://www.yelp.com/biz/the-face-shop-santa-clara','http://www.yelp.com/biz/trader-joes-mountain-view']

from scrapy.spider import BaseSpider
from scrapy.http import Request
from urlparse import urljoin
from scrapy.selector import HtmlXPathSelector
from yelp.items import YelpItem
import psycopg2
from datetime import datetime


""" Database Creation"""
try:
	con = psycopg2.connect(database="mm", user="postgres", password="mercuryminds", host="localhost")
	cur = con.cursor()
except:
	""" Database not Connected """

class YelpSpider(BaseSpider):
	

	name = "ylpp"
	start_urls=[url[i]+'?sort_by=date_desc' for i in range(len(url))]
#	f=open('opt.csv','w')

	def parse(self, response):
		
		itm=[]
		hxs = HtmlXPathSelector(response)
		item = YelpItem()	 
		item['bid'] = 0
		item['url'] = response.url

		"""Getting the Business Id from the DB if exists """

		qu = ("select distinct u from y")
		cur.execute(qu)
		rows = cur.fetchall()
		li = [r[0] for r in rows]
#		print li
		for i in range(len(li)):
	#		print li[i], item['url']
			if li[i].split('?')[0] in item['url']:
				qu1 = ("select distinct id from y where u='%s'")%li[i]
				cur.execute(qu1)
				rows1= cur.fetchall()
				li1=[i[0] for i in rows1]
	#			print li1				
				if len(li1) > 0:
					item['bid'] = li1[0]
		""" Maximum Date has been verified from the DB through bid """

		qu2 = ("select max(d) from y where id =%d")%item['bid']
		cur.execute(qu2)
		rows2=cur.fetchall()
		max_date = [i[0] for i in rows2][0]
	
#		print max_date
		

		if item['bid'] > 0:
			print " ID assigned"
		else:
			item['bid'] = input("Enter the Business Id here for URL:       %s        : "%item['url'])
			max_date = datetime.strptime('','')
			print max_date

		print item['bid']




		item['rating'] = float(hxs.select('//div[@itemprop="aggregateRating"]/div/meta/@content').extract()[0].encode('ascii', 'ignore').strip())
		item['rv_count'] = int(hxs.select('//span[@itemprop="reviewCount"]/text()').extract()[0].encode('ascii', 'ignore').strip())
	
		if item['rv_count'] > 0:

			no = len(hxs.select('//div[@itemprop="review"]').extract())
			x=hxs.select('//div[@class="review-list"]/ul/li')
			for i in range(no):


				try:
					item['rv_date'] = x[0].select('//meta[@itemprop="datePublished"]/@content').extract()[i].encode('ascii', 'ignore').strip()
				except:
					item['rv_date'] = 'NULL'

				current_date = datetime.strptime(item['rv_date'],'%Y-%m-%d')				

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
#				print current_date,max_date
				last_date = current_date
				

				""" It Only insert the new Feeds """
			
				if current_date >= max_date:

					sql = ("insert into y select '%s','%s','%s','%s','%s','%s','%s','%s' where not exists ( select * from y where dc='%s' and p='%s')"%(item['bid'],item['url'],item['rating'],item['rv_count'],item['rv_date'],item['rv_profile'],item['rv_dc'],item['rv_rating'],item['rv_dc'],item['rv_profile']))

					cur.execute(sql)
		                	con.commit()
				
				else:
					break
					print "No updated review are here"
				
				
				print item['url'],item['rv_profile']




			"""Check the New reviews is in next page and it will not include newly entered url """

			if item['rv_count'] > 40 and last_date > max_date and '1900-01-01 00:00:00' not in str(max_date):				
			
				nxt_link = []

				""" Parse the nex review link by multiple of 40"""


				if float(item['rv_count'])/40 > item['rv_count']/40:
					x= range(40,(item['rv_count']/40)*40+1,40)
					for i in range(len(x)):
						nxt_link.append(hxs.select('//a[@class="page-option prev-next"]/@href').extract()[0].encode('ascii', 'ignore').split('?')[0]+'?start=%s'%x[i]+'&sort_by=date_desc')
				else:					
					x= range(40,(item['rv_count']/40-1)*40+1,40)
					for i in range(len(x)):
						nxt_link.append(hxs.select('//a[@class="page-option prev-next"]/@href').extract()[0].encode('ascii', 'ignore').split('?')[0]+'?start=%s'%x[i]+'&sort_by=date_desc')

				print nxt_link

				for i in range(len(nxt_link)):
					if nxt_link[i]:
						""" Next link Processed """
						yield Request( nxt_link[i], callback=self.parse)


			elif item['rv_count'] > 40 and '1900-01-01 00:00:00' in str(max_date):				

				nxt_link = []

				""" Parse the nex review link by multiple of 40"""

				"""Check the reviews is in next page it works only for the new url """

				if float(item['rv_count'])/40 > item['rv_count']/40:
					x= range(40,(item['rv_count']/40)*40+1,40)
					for i in range(len(x)):
						nxt_link.append(hxs.select('//a[@class="page-option prev-next"]/@href').extract()[0].encode('ascii', 'ignore').split('?')[0]+'?start=%s'%x[i]+'&sort_by=date_desc')
				else:					
					x= range(40,(item['rv_count']/40-1)*40+1,40)
					for i in range(len(x)):
						nxt_link.append(hxs.select('//a[@class="page-option prev-next"]/@href').extract()[0].encode('ascii', 'ignore').split('?')[0]+'?start=%s'%x[i]+'&sort_by=date_desc')

				print nxt_link

				for i in range(len(nxt_link)):
					if nxt_link[i]:
						""" Next link Processed """
						yield Request( nxt_link[i], callback=self.parse_sub)
				
			else:

				print "Do nothing"

				""" Reviews below 40 for this business"""
				
		else:
			item['rv_date'] = 'NULL'
			item['rv_profile'] = 'NULL'
			item['rv_rating'] = 'NULL'
			item['rv_dc'] = 'NULL'

	""" Parse_sub function is only for the URL which is running first time alone"""

	def parse_sub(self, response):


		print "Sub parse Called "
		itm=[]
		hxs1 = HtmlXPathSelector(response)
		item = YelpItem()	 
		item['bid'] = 0
		item['url'] = response.url

		"""Getting the Business Id from the DB if exists """

		qu = ("select distinct u from y")
		cur.execute(qu)
		rows = cur.fetchall()
		li = [r[0] for r in rows]
#		print li
		for i in range(len(li)):
	#		print li[i], item['url']
			if li[i].split('?')[0] in item['url']:
				qu1 = ("select distinct id from y where u='%s'")%li[i]
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




		item['rating'] = float(hxs1.select('//div[@itemprop="aggregateRating"]/div/meta/@content').extract()[0].encode('ascii', 'ignore').strip())
		item['rv_count'] = int(hxs1.select('//span[@itemprop="reviewCount"]/text()').extract()[0].encode('ascii', 'ignore').strip())
	
		if item['rv_count'] > 0:

			no = len(hxs1.select('//div[@itemprop="review"]').extract())
			x=hxs1.select('//div[@class="review-list"]/ul/li')
			for i in range(no):


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


				sql = ("insert into y select '%s','%s','%s','%s','%s','%s','%s','%s' where not exists ( select * from y where dc='%s' and p='%s')"%(item['bid'],item['url'],item['rating'],item['rv_count'],item['rv_date'],item['rv_profile'],item['rv_dc'],item['rv_rating'],item['rv_dc'],item['rv_profile']))

				cur.execute(sql)
	                	con.commit()
				
				
				
	#			print item['url'],item['rv_profile']


			if item['rv_count'] > 40:				
				nxt_link = []

				""" Parse the nex review link by multiple of 40"""


				if float(item['rv_count'])/40 > item['rv_count']/40:
					x= range(40,(item['rv_count']/40)*40+1,40)
					for i in range(len(x)):
						nxt_link.append(hxs1.select('//a[@class="page-option prev-next"]/@href').extract()[0].encode('ascii', 'ignore').split('?')[0]+'?start=%s'%x[i]+'&sort_by=date_desc')
				else:					
					x= range(40,(item['rv_count']/40-1)*40+1,40)
					for i in range(len(x)):
						nxt_link.append(hxs1.select('//a[@class="page-option prev-next"]/@href').extract()[0].encode('ascii', 'ignore').split('?')[0]+'?start=%s'%x[i]+'&sort_by=date_desc')
				print nxt_link
				for i in range(len(nxt_link)):
					if nxt_link[i]:
						""" Next link Processed """
						yield Request( nxt_link[i], callback=self.parse_sub)
				
			else:

				print "Do nothing"

				""" Reviews below 40 for this business"""
				
		else:
			item['rv_date'] = 'NULL'
			item['rv_profile'] = 'NULL'
			item['rv_rating'] = 'NULL'
			item['rv_dc'] = 'NULL'


