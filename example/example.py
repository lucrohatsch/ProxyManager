import requests
from src.proxy_manager import Proxy, ProxyRepository

pxy_repo = ProxyRepository()
pxy_repo.create_repository_from_json_file('proxies.json')

for pxy in pxy_repo.list:
    if pxy.is_proxy_working():
        print(pxy.__dict__)
    else:
        print(f"Proxy {pxy.ip} is not working")
