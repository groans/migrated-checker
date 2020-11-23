import requests
import string
import json
import sys
from termcolor import colored
from threading import Thread
from itertools import cycle
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import MaxRetryError
from requests.packages.urllib3.exceptions import ProxyError as urllib3_ProxyError

# Old JSON support. Moved to plaintext to make more user-friendly.
#names = json.loads(open('accounts.json').read())
#proxies = json.loads(open('proxies.json').read())

with open("accounts.txt", "r+") as f:
    names = [x.strip() for x in f.readlines()]

with open("proxies.txt", "r+") as f:
    proxies = [x.strip() for x in f.readlines()]

uuidURL = "https://api.mojang.com/users/profiles/minecraft/"
migratedURL = "https://sessionserver.mojang.com/session/minecraft/profile/"
total = len(names)
num = 1
proxy_pool = cycle(proxies)

def checkMigration(name, uuid, proxy):
	attempt = num + 1
	percentage = round(attempt / total, 3)
	percentage = percentage * 100
	urlResponse = requests.get(migratedURL + uuid, proxies={"http": "http://"+proxy, "https": "https://"+proxy}, timeout=2).json()
	try:
		isLegacy = urlResponse["legacy"]
		file = open("unmigrated.txt", "a")
		file.write(name+"\n")
		file.close()
		print("(" + str(attempt) + "/" + str(total) + "| " + str(percentage) + "%) Checking " + name + " for unmigrated status... [" + colored("UNMIGRATED", "green") + "] Proxy: " + proxy)
	except (KeyError, IndexError):
		print("(" + str(attempt) + "/" + str(total) + "| " + str(percentage) + "%) Checking " + name + " for unmigrated status... [" + colored("MIGRATED", "red") + "] Proxy: " + proxy)

def getUUID(name, proxy, i=[0]):
	attempt = num + 1
	percentage = round(attempt / total, 3)
	percentage = percentage * 100
	try:
		urlResponse = requests.get(uuidURL + name, proxies={"http": "http://"+proxy, "https": "https://"+proxy}, timeout=10).json()
		uuid = urlResponse["id"]
		checkMigration(name, uuid, proxy)
		i[0] = 0
	except (ValueError, KeyError, IndexError):
		i[0] = 0
		print("(" + str(attempt) + "/" + str(total) + "| " + str(percentage) + "%) Checking " + name + " for unmigrated status... [" + colored("INVALID", "red") + "] Proxy: " + proxy)
	except (ConnectionError, OSError):
		i[0]+=1
		if i[0] == len(proxies):
			sys.exit("No proxies could establish a connection. Try new proxies and a larger proxylist.")
		#print("Proxy error (rate limited?). Cycling proxy.")
		getUUID(name, getWorkingProxy())

def getWorkingProxy():
  proxy = next(proxy_pool)
  try:
    request = requests.get("http://ipinfo.io/json", proxies={"http": "http://"+proxy, "https": "https://"+proxy}, timeout=1).json()
    return proxy
  except Exception as e:
    return getWorkingProxy()

if __name__ == '__main__':
	thread_list = []
	count = 0
	print("")
	print("Checking all cape accounts for 'unmigrated' status...")
	print("Made by Landon. Landon#1718, @Religion on MC-Market.")
	print("")
	print(colored("All usernames loaded! (accounts.txt)", "green"))
	print(colored("All proxies loaded! (proxies.txt)", "green"))
	for name in names:
	  thread_list.append(Thread(target=getUUID, args=(name, getWorkingProxy())))
	  thread_list[len(thread_list)-1].start()
	  count += 1
	  num += 1
	for x in thread_list:
	  x.join()
	print("Completed.")
