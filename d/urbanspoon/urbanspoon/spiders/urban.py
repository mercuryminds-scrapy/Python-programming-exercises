""" Enter Url here"""
#url =['http://www.urbanspoon.com/r/35/1571097/restaurant/Hampton-Roads/Dam-Neck-Corner-Pungo/Firebrew-Virginia-Beach']
url =['http://www.urbanspoon.com/r/1/4524/restaurant/Capitol-Hill/Honey-Hole-Sandwiches-Seattle','http://www.urbanspoon.com/r/35/1571097/restaurant/Hampton-Roads/Dam-Neck-Corner-Pungo/Firebrew-Virginia-Beach','http://www.urbanspoon.com/r/13/169913/restaurant/North-Richland-Hills-Richland-Hills/Texs-Star-Grill-Watauga']
from scrapy.spider import BaseSpider
from urlparse import urljoin
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from urbanspoon.items import UrbanspoonItem
import psycopg2


""" Database Creation"""
try:
	con = psycopg2.connect(database="mm", user="postgres", password="mercuryminds", host="localhost")
	cur = con.cursor()
except:
	""" Database not Connected """

class UrbanspoonSpider(BaseSpider):
	
	name = "urban"

#	allowed_domains = ["urbanspoon.com"]
	start_urls=[url[i] for i in range(len(url))]

#	filehandle = open('Urbanspoon.csv','w')
#	filehandle.write("Manufacturer\tDescription\tPart Number\tUrl\tAvailability\tPrice\tItem Number\tOEM\tMore_items\n")
	
	def parse(self,response):

		item=UrbanspoonItem()
		hxs = HtmlXPathSelector(response)
		item['url']= response.url
		item['b_id'] = 0

		"""Getting the Business Id from the DB if exists """

		qu = ("select distinct url from social_data.urbanspoon")
		cur.execute(qu)
		rows = cur.fetchall()
		li = [r[0] for r in rows]
#		print li

		for i in range(len(li)):
	#		print li[i], item['url']
			if li[i] in item['url']:
				qu1 = ("select distinct business_id from social_data.urbanspoon where url='%s'")%li[i]
				cur.execute(qu1)
				rows1= cur.fetchall()
				li1=[i[0] for i in rows1]
#				print li1				
				if len(li1) > 0:
					item['b_id'] = li1[0]
		if item['b_id'] > 0:
			print " ID assigned"
		else:
			item['b_id'] = input("Enter the Business Id here for URL:       %s        : "%item['url'])


		print item['b_id']


		
		item['n_votes'] = hxs.select('//div[@class="stats"]/div/text()').extract()[0].encode('utf-8').replace('\n','').strip()
		item['p_like']	= hxs.select('//div[@class="rating"]/text()').extract()[0].encode('utf-8').strip()
		item['n_reviews'] = int(hxs.select('//div[@class="stats"]/div/a[@data-ga-action="reviews"]/text()').extract()[0].split(' ')[0].encode('utf-8').strip())
		nxt_link = 'http://www.urbanspoon.com'+hxs.select('//div[@data-ga-action="diner-reviews"]/@data-url').extract()[0].encode('utf-8').strip()
		print nxt_link
		if nxt_link:
			yield Request(nxt_link, callback=self.parse_sub, meta=dict(item=item))
	
	def parse_sub(self,response):


		print "Sub Parse Called"
		item = response.meta.get('item')
		hxs = HtmlXPathSelector(response)

		x=hxs.select('//ul/li[@class="comment review"]')
		length=len(x[0].select('//div[@class="details"]/div[@class="byline"]/a[@itemprop="reviewer"]/text()').extract())

		for i in range(length):
					
			try:
				item['date']  = x[0].select('//div[@class="details"]/div/time[@class="posted-on"]/text()').extract()[i].encode('utf-8').split(' ')[2].replace('\n','')
				
			except:
				item['date'] = ''
			try:
				item['title'] = x[0].select('//div[@class="details"]/div[@class="title"]/text()').extract()[i].encode('utf-8').replace("'","").strip()
			except:
				item['title'] = ''
				
			try:
				item['description'] = x[0].select('//div[@class="details"]/div[@itemprop="description"]').extract()[i].encode('utf-8').split('\n')[1].replace("'","")
			except:
				item['description'] = ''
			try:
				item['user'] = x[0].select('//div[@class="details"]/div[@class="byline"]/a[@itemprop="reviewer"]/text()').extract()[i].encode('utf-8').replace("'","").strip()
			except:
				item['user'] = ''
			print item['user']
			sql = ("insert into social_data.urbanspoon select '%s','%s','%s','%s','%s','%s','%s','%s','%s' where not exists ( select * from social_data.urbanspoon where review_description='%s' and review_user='%s')"%(item['b_id'],item['url'],item['n_votes'], item['p_like'], item['n_reviews'],item['date'],item['title'],item['description'], item['user'],item['description'], item['user']))
		        cur.execute(sql)
		        con.commit()

		

