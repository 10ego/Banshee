import requests
import sys

preurl = "https://gimmeproxy.com/api/getProxy?anonymityLevel=1&user-agent=true"
def pre_proxy(proxy={}):
	global preurl
	pre = requests.get(preurl)
	if pre.status_code == 200:
		proxy['http'] = "%s://%s:%s" % (pre.json()['protocol'],pre.json()['ip'],pre.json()['port'])
		proxy['https'] = "%s://%s:%s" % (pre.json()['protocol'],pre.json()['ip'],pre.json()['port'])
#		print("initializing proxy retrieved") 
		return proxy
	else:
		return pre_proxy()


url = "https://api.getproxylist.com/proxy?anonymity[]=high%20anonymity&anonymity[]=transparent"
#lastWorkingProxy = pre_proxy()
c = 0
def getProxy(proxy, country = None):
	global lastWorkingProxy
	global url
	global preurl
	global c
	suburl = ""
	if country != None:
		suburl = "&country=%s" % (country)
	try:
		r = requests.get(url+suburl, proxies = proxy)
		if r.status_code == 200:
#			lastWorkingProxy = proxy
			d = r.json()
			proxy = {}
			proxy['http'] = "%s://%s:%s" % (d['protocol'], d['ip'], d['port'])
			proxy['https'] =  "%s://%s:%s" % (d['protocol'], d['ip'], d['port'])
			return proxy
		else:
			if c>5:
				url = preurl
			print("Failed to retrieve functional proxy, trying again..1")
			proxy = pre_proxy()
			c+=1
			return getProxy(proxy, country)
		
	except Exception as e:
		if c>5:
			url = preurl
		print("Failed to retrieve functional proxy, trying again..2")
		proxy = pre_proxy()
		c+=1
		return getProxy(proxy, country)

def hopProxy(hops, country, proxy=pre_proxy(), errswitch = False):
	global url
	if errswitch == False:
		for x in range(hops-1):
			proxy = getProxy(proxy, country)
			print("Hopping %i of %i.." % (x+1, hops))
		print("Making the final hop %i of %i.." % (hops, hops))
	
	proxy = getProxy(proxy, country) #Final hop & exit proxy from declared country
	try:
		r = requests.get(url, proxies=proxy)
		if r.status_code==200:
			return proxy
		else:
			proxy = pre_proxy()
			return hopProxy(1, country, proxy, errswitch = True)
	except:
		proxy = pre_proxy()
		return hopProxy(1, country, proxy, errswitch = True)

def scrapeHTML(data_url, proxy, formarg=None):
	
	try:
		s = requests.get(data_url, proxies = proxy)
		if s.status_code == 200:
			if formarg == "-json":
				data = s.json()
			elif formarg == None:
				data = s.text
			else:
				data = s.text
				print("%s not recognized. Defaulting to text scrape" % (arg2))
			return data, proxy
		else:
			print("Error code: %d" % (s.status_code))
	except Exception as e:
		print(type(e), e.args, "Check your URL again")

scrape_url = str(sys.argv[1])
hop_count = int(sys.argv[2])
country_code = str(sys.argv[3]).upper()
format_arg = str(sys.argv[4])
#python3 banshee.py scrape_url hop_count country_code format_arg

outdata, final_proxy = scrapeHTML(data_url = scrape_url, proxy=hopProxy(hop_count, country_code), formarg=format_arg)

print("Exit node proxy: %s" % (final_proxy))
print(outdata)
