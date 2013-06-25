import httplib, re, sys, traceback
from bs4 import BeautifulSoup

#urlTemplate="/s/ref=PIVHPBB_Dept_Movies?ie=UTF8&rh=n%%3A2858905011%%2Cp_85%%3A2470955011&page=%d&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=left-1&pf_rd_r=1N8CV42TQ52BYM9KC6NC&pf_rd_t=101&pf_rd_p=1346922482&pf_rd_i=2676882011"
#n = 1
#startingurl = urlTemplate % (n,)
startingurl = "/s/ref=PIVHPBB_Dept_Movies?ie=UTF8&rh=n%3A2858905011%2Cp_85%3A2470955011&page=1&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=left-1&pf_rd_r=1N8CV42TQ52BYM9KC6NC&pf_rd_t=101&pf_rd_p=1346922482&pf_rd_i=2676882011"
host="www.amazon.com"

def GetWebContent(url):
    conn.request("GET",url)
    r1 = conn.getresponse()
    return r1.read()

def ParseContent(content):
    soup = BeautifulSoup(content)
    NextPage = "error"
    for aa in soup.find_all('span','pagnNext'):
	bb = aa.find('a')
	if bb is not None and bb.has_key('href'): 
	    NextPage = bb['href']

	
    for aa in soup.find_all('div'):
	if aa.has_key('class') and aa['class'][0] == "result":
	    Number = aa.find('div','number').string
	    Data = aa.find('div','data')
	    Data2 = Data.find('h3','title')
	    Title = Data2.find('a').string
	    Starring = ""
	    StarringTag = Data2.find('span','starring')
	    if StarringTag is not None:
		Starring = StarringTag.string
	    URL = 'error'
	    URLp = Data2.find('a')
	    if URLp is not None and URLp.has_key('href'):
		URL = URLp['href']
	    Data3 = Data.find('div','starsAndPrime')
	    Rating = 'error'
	    if Data3 is not None:
		Data4 = Data3.find('div','stars')
		Rating = Data4.find('a').get('alt')
	    Data4a = Data.find('div','mvOneCol')
	    Data5 = None
	    if Data4a is not None:
		Data4b = Data4a.find('div','secondRow')
		if Data4b is not None:
		    Data4c = Data4b.find('div','indent')
		    if Data4c is not None:
			Data5 = Data4c.find('div','priceListFirstSet')
	    if Data5 is not None:
		if Data5.find('span','priceFirstLabel').find('a').string == \
		    'Prime members':
		# we have the right price
		    PriceP = Data5.find('span','price')
		    if PriceP is not None:
			try:
			    Price = PriceP.string.encode('ascii','ignore')
			except:
			    print('could not encode '+PriceP.string)
			    Price = 'unk'
		    else:
			Price = "unk"
	    else:
		Price = "unk"

	    # final cleanup to avoid errors
	    try:
		Numberx = str(Number)
	    except:
		Numberx = 'error: '+repr(Number)
	    try:
		Titlex = str(Title)
	    except:
		Titlex = 'error: '+repr(Title)
	    try:
		Ratingx = str(Rating)
	    except:
		Ratingx = 'error: '+repr(Rating)
	    try:
		Pricex = str(Price)
	    except:
		Pricex = 'error: '+repr(Price)
	    try:
		Starringx = str(Starring)
	    except:
		Starringx = 'error: '+repr(Starring)
	    try:
		URLx = str(URL)
	    except:
		URLx = 'error: '+repr(URL)

	    fp.write("\t".join([Numberx,Titlex,Ratingx,Pricex,Starringx,URLx]))
	    fp.write("\n")
    return NextPage


fp = open('AmazonData.tab','w')
conn = httplib.HTTPConnection(host)
url = startingurl
cnt = 1
while True:
    try:
	content = GetWebContent(url)
    except:
	print('Exception on GetWebContent for url\n'+url)
	print("Exception type: %s, Exception arg: %s\nException Traceback:\n%s" %  \
                    (sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
	traceback.print_tb(sys.exc_info()[2])
	break
    # if len(url) > 40: url = url[0:36]+'...'
    print('Page %s, url %s' % (cnt,url))
    try:
	url = ParseContent(content)
    except:
	print('Exception on ParseContent')
	print("Exception type: %s, Exception arg: %s\nException Traceback:\n%s" %  \
                    (sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
	traceback.print_tb(sys.exc_info()[2])
	fp2 = open('Exception.htm','w')
	fp2.write(content)
	fp2.close()
	break
    cnt += 1
fp.close()
conn.close()
