import urllib, urllib2, cookielib

#cookie storage
cj = cookielib.CookieJar()
#create an opener
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#Add useragent, sites don't like to interact programs.
opener.addheaders.append(('User-agent', 'Mozilla/4.0'))
opener.addheaders.append( ('Referer', 'https://www.hscripts.com/tools/mailid-validation/') )

login_data = urllib.urlencode({'email' : 'office@mos.org', 'start' : 'go'
                               })
#
resp = opener.open('https://www.hscripts.com/tools/mailid-validation/', login_data)
the_page = resp.read()

file = open('outpu.html','w')
file.write(the_page)
file.close()
resp.close()

