import requests
from bs4 import BeautifulSoup as BS

class Banshee():
    def __init__(self):
        proxy_feed = "https://free-proxy-list.net/anonymous-proxy.html"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"
        r = requests.get(proxy_feed, headers={"User-Agent":user_agent})

        if r.status_code == 200:
            raw_proxy = r.text
            soup_proxy = BS(raw_proxy, 'html.parser')
            self.proxy_list = soup_proxy.find('table', {"id":"proxylisttable"})
            print("Proxy list refreshed")
        else:
            raise HTTPError("Status code:"+r.status_code)
        self.proxyCounter = 0
        self.tablebuilt = False

    def tableDataText(self, table):
        rows = []
        trs = table.find_all('tr')
        headerrow = [td.get_text(strip=True) for td in trs[0].find_all('th')]
        if headerrow:
                trs = trs[1:]

        for tr in trs:
            rows.append([td.get_text(strip=True) for td in tr.find_all('td')])
        return headerrow, rows

    def buildTable(self):
        d = {}
        header, table = self.tableDataText(self.proxy_list)
        d['header'] = header
        d['data'] = table
        self.full_proxy_list = d['data']
        self.maxProxy = len(self.full_proxy_list)
        self.tablebuilt = True
        
    def nextProxy(self):
        if not self.tablebuilt:
            self.buildTable()

        if self.proxyCounter <= self.maxProxy:
            proxy_data = self.full_proxy_list[self.proxyCounter]
            if proxy_data[6] == 'yes':
                https = proxy_data[0] + ":" + proxy_data[1]
                self.proxyCounter+=1
                print(https)
                return {"https":https}
            else:
                self.proxyCounter+=1
                self.nextProxy()
