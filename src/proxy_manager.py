import requests
import json

class Proxy:
    def __init__(self, proxy: dict):
        self.name = proxy.get('name')
        self.ip = proxy.get('ip')
        self.port = proxy.get('port')
        self.user = proxy.get('user')
        self.pss = proxy.get('pass')
    
    def str_proxy(self) -> dict:
        """
        Given a single proxy, from the .json file:
        Return the proxy string necessary to pass as parameter
        to a requests.request() constructor.
        """
        if self.user:
            return {
                "http": f'http://{self.user}:{self.pss}@{self.ip}:{self.port}',
            	"https": f'https://{self.user}:{self.pss}@{self.ip}:{self.port}'
            }
        else:
            return {
                {"http": f'http://{self.ip}:{self.port}',
            	"https": f'https://{self.ip}:{self.port}'
            }

    def is_proxy_working(self)->bool:
        p = {
        'http': f'http://{self.user}:{self.pss}@{self.ip}:{self.port}',
        'https': f'http://{self.user}:{self.pss}@{self.ip}:{self.port}'
        }
        r = requests.get(url='https://api.myip.com/', proxies=p)
        print(r.text)
        if self.ip in r.content.decode('utf-8'):
            return True
        return False

class ProxyRepository:
    def __init__(self):
        self.list = []

    def add_proxy(self, proxy: Proxy):
            self.list.append(proxy)

    def create_repository_from_json_file(self, path: str)->list:
        """Creates a list with all proxies.

        Args:
            path: to json file with proxies

        Returns:
            list: with all proxies
        """
        with open(path) as f:
            pxy_file = json.loads(f.read())
        for proxy in pxy_file['proxies']:
            self.list.append(Proxy(proxy))
        
        
    def switch_proxy(self, current: Proxy = None) -> Proxy:
        """
        Given a list of proxies in a .json file:
        Return the next one (if you pass the current one),
        Return the first one (if nothing is passed), or
        Return None (ie, if the file is empty or doesn't exist)
        """
        if len(self.list) == 0:
            return None
        if not current:
            return self.list[0]
        found = -1
        for i, p in enumerate(self.list):
            if p["ip"] == current["ip"]:
                found = i
                break
        if found < 0 or i+1 == len(self.list):
            return self.list[0]
        else:
            return self.list[i+1]