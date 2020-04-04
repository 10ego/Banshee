# Banshee

Proxy hop to be used with requests.

Example:

```
from banshee import Banshee
import requests

url = "https://some.url"

banshee = Banshee()
proxy = banshee.nextProxy()
r = requests.get(url, proxies = proxy)
```
