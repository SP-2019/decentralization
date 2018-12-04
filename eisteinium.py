import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib.request
import urllib.parse

miners=[]
stats=[]

for j in range(1000):
	
	page='https://chainz.cryptoid.info/emc2/block.dws?'+str(2026328-j)+'.htm'
	page=requests.get(page)
	html = page.text
	while html.find('wait 5')!=-1:
		sleep(360)
		page='https://chainz.cryptoid.info/emc2/block.dws?'+str(2026328-j)+'.htm'
		page=requests.get(page)
		html = page.text
	i=html.find("extracted by")

	if i==-1:
		page='https://chainz.cryptoid.info/emc2/api.dws?q=getblockhash&height='+str(2026328-j)
		page=requests.get(page)
		html = page.text
		while html.find('wait 5')!=-1:
			sleep(360)
			page='https://chainz.cryptoid.info/emc2/api.dws?q=getblockhash&height='+str(2026328-j)
			page=requests.get(page)
			html = page.text
		bxhash=html[1:-1]
		page='https://chainz.cryptoid.info/explorer/block.txs.dws?coin=emc2&h='+bxhash+'.js'
		page=requests.get(page)
		html = page.text
		
		while html.find('wait 5')!=-1:
			sleep(360)
			page='https://chainz.cryptoid.info/explorer/block.txs.dws?coin=emc2&h='+bxhash+'.js'
			page=requests.get(page)
			html = page.text

		value=0
		while float(value)<2:
			i = html.find('"a":')
			html=html[i+5:]
			i1=html.find('"')
			miner=html[:i1]
			i=html.find('"v":')
			html=html[i+4:]
			i=html.find('}')
			value=html[:i]
	else:
		html=html[i:]
		i=html.find('>')
		html=html[i+1:]
		i=html.find('<')
		miner=html[:i]
		
	print(j)
	if miner not in miners:
		miners.append(miner)
		stats.append(1)
	else:
		k=miners.index(miner)
		stats[k]=stats[k]+1
	
print(miners)
print (stats)	