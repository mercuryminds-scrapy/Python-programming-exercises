" Enter Url here"


url =['http://www.tripadvisor.com/Restaurant_Review-g42251-d4164754-Reviews-Taboon-Grand_Blanc_Michigan.html','http://www.tripadvisor.com/Restaurant_Review-g28970-d2137408-Reviews-Lincoln_DC-Washington_DC_District_of_Columbia.html','http://www.tripadvisor.com/Restaurant_Review-g29556-d416774-Reviews-Zingerman_s_Delicatessen-Ann_Arbor_Michigan.html','http://www.tripadvisor.com/Restaurant_Review-g58277-d3529482-Reviews-FireBrew-Virginia_Beach_Virginia.html']

from scrapy.spider import BaseSpider
from scrapy.http import Request
from urlparse import urljoin
from scrapy.selector import HtmlXPathSelector
from trip.items import TripItem
import psycopg2
from datetime import datetime


""" Database Creation"""
try:
	con = psycopg2.connect(database="mm", user="postgres", password="mercuryminds", host="localhost")
	cur = con.cursor()
except:
	""" Database not Connected """

class YelpSpider(BaseSpider):
	

	name = "trip"
	start_urls=[url[i] for i in range(len(url))]

	def parse(self, response):
		
		itm=[]
		hxs = HtmlXPathSelector(response)
		item = TripItem()	 
		item['bid'] = 0
		item['url'] = response.url

		"""Getting the Business Id from the DB if exists """

		qu = ("select distinct u from social_data.tripadvisor1")
		cur.execute(qu)
		rows = cur.fetchall()
		li = [r[0] for r in rows]
#		print li
		for i in range(len(li)):
#			print li[i], item['url']
			try:
				lis=li[i].split('-or')[1].split('-')[1]
			except:
				lis=li[i].split('Reviews-')[1].split('-')[0]
			if item['url'].find(lis)>0:
				qu1 = ("select distinct id from social_data.tripadvisor1 where u='%s'")%li[i]
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




		item['rating'] = float(hxs.select('//div[@class="rs rating"]/span/img/@content').extract()[0].encode('ascii', 'ignore').strip())
		item['rv_count'] = int(hxs.select('//div[@class="rs rating"]/a/span/text()').extract()[0].encode('ascii', 'ignore').strip())
	
		if item['rv_count'] > 0:

			no = len(hxs.select('//div[@class="reviewSelector "]').extract())

			for i in range(no):
#				cur.execute("select max(d) from social_data.tripadvisor1 where id='%s'" %item['bid'])
#				r = cur.fetchall()
#				m_dt = r[0][0]		
				
				try:
					xd=hxs.select('//span[@class="ratingDate"]').extract()[i].encode('utf-8').split('Reviewed')[1].split('\n')[0].replace(',','').replace('\n','').strip()
					date=datetime.strptime(xd,'%B %d %Y')
					item['rv_date'] =str(date)
					

				except:
					date=datetime.strptime('9999-01-01','%Y-%d-%m')
					item['rv_date'] = '0001-01-01 00:00:00'
				
				try:
					item['rv_profile'] = hxs.select('//div[@class="username mo"]/span/text()').extract()[i].encode('ascii', 'ignore').replace('.','').replace("'"," ").strip()
				except:
					item['rv_profile'] = 'NULL'
				
				try:
					item['rv_heading'] =  hxs.select('//span[@class="noQuotes"]/text()').extract()[i].encode('ascii', 'ignore').replace('.','').replace("'"," ").strip()
				except:
					item['rv_heading'] = 'NULL'

				try:
					item['rv_rating'] =  float(hxs.select('//div[@class="rating reviewItemInline"]/span/img/@alt').extract()[i].encode('ascii', 'ignore').split(' ')[0].strip())
				except:
					item['rv_rating'] = '0.0'
				try:
					item['rv_dc'] =  hxs.select('//p[@class="partial_entry"]').extract()[i].encode('ascii', 'ignore').split('\n')[1].replace("'"," ").replace('.','').strip()
				except:					
					item['rv_dc'] = 'NULL'
#				if date >= m_dt:
				sql = ("insert into social_data.tripadvisor1 select '%s','%s','%s','%s','%s','%s','%s','%s','%s' where not exists ( select * from social_data.tripadvisor1 where dc='%s' and p='%s')"%(item['bid'],item['url'],item['rating'],item['rv_count'],item['rv_date'],item['rv_heading'],item['rv_rating'],item['rv_dc'],item['rv_profile'],item['rv_dc'],item['rv_profile']))
#				else:
#					break	
		
				cur.execute(sql)
	                	con.commit()

				print item['url'],item['rv_profile']


			""" Parse Next link"""


			
			try:
				link = hxs.select('//div[@class="pgLinks"]/a[@class="guiArw sprite-pageNext "]/@href').extract()[0].encode('ascii', 'ignore').strip()	
				nxt_link = urljoin(response.url,link)
			except:
				nxt_link = []
			
			

			print nxt_link
			
			if nxt_link:
				""" Next link Processed """
				yield Request( nxt_link, callback=self.parse)
			else: 
				print " Progress Completed "
				
			
				
		else:
			item['rv_date'] = 'NULL'
			item['rv_profile'] = 'NULL'
			item['rv_rating'] = 'NULL'
			item['rv_dc'] = 'NULL'
			item['rv_heading'] = 'NULL'




