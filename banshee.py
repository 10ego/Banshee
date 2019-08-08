import requests
import sys
import rand
class Banshee()
	def __init__(self):
		self.preurl = "https://gimmeproxy.com/api/getProxy?anonymityLevel=1&user-agent=true"
		self.hopurl = "https://www.proxy-list.download/api/v1/get?type=http&anon=elite&country=US" 
		self.session = requests.session()

	def init_proxy(self):
		pr = self.session.get(self.preurl)
		proxy = {}
		if pr.status_code == 200:
			proxy['http'] = "{}://{}:{}".format(pr.json()['protocol'], pr.json()['ip'], pr.json()['port'])
			proxy['https'] = "{}://{}:{}".format(pr.json()['protocol'], pr.json()['ip'], pr.json()['port'])
	#		print("initializing proxy retrieved") 
		else:
			self.init_proxy()
		self.layer1 = proxy

	def get_mask(self, init_proxy = self.layer1):
		pr = requests.get(self.hopurl, proxies = init_proxy)
		proxy = {}
		if pr.status_code == 200:
			self.hop_list = pr.text.splitlines()

	def veil(self):
		proxy = {}
		for i in self.hop_list:
			if self.session.get(self.hop_list[i]).status_code==200:
				proxy['http'] = 'http://{}'.format(self.hop_list[i])
				proxy['https'] = 'https://{}'.format(self.hop_list[i])
				break
			else:
				proxy = self.layer1
		return proxy

