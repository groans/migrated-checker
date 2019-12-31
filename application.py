import requests
import os
import string
import json
import traceback
import socket
import concurrent
from itertools import cycle
from multiprocessing import Pool

def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 


names = json.loads(open('accounts.json').read())
proxies = json.loads(open('proxies.json').read())
url = 'https://namemc.com/profile/'

def checkMigration(name):
	proxy_pool = cycle(proxies)
	while True:
		try:
			proxy = next(proxy_pool)
			r = requests.get(url + name, proxies={"http": proxy, "https": proxy})
			print("Checking " + name + " for unmigrated status.")
			if "Unmigrated" in r.text:
				file = open("accounts.txt", "a")
				file.write(name)
				file.close()
				prGreen("ACCOUNT UNMIGRATED :) (accounts.txt))")
			else:
				prRed("ACCOUNT MIGRATED :(")
		except:
			print("Connection error. Retrying...")
			proxy = next(proxy_pool)
			continue
		break

if __name__ == '__main__':
	print("")
	print("Checking all cape accounts for 'unmigrated' status...")
	print("Made by Landon. Landon#1000, @Religion on MC-Market.")
	print("")
	prGreen("All usernames loaded! (accounts.json)")
	prGreen("All proxies loaded! (proxies.json)")
	print("Proxies are being cycled...")
	pool = Pool()
	pool.map(checkMigration, names)

#if __name__ == '__main__':
	#executor = concurrent.futures.ProcessPoolExecutor(10)
	#futures = [executor.submit(checkMigration, name) for name in names]
	#concurrent.futures.wait(futures)
