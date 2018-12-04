import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib.request
import urllib.parse

miners=[]
stats=[]

for j in range(1000):
	page='https://explorer.nebl.io/api/getblockhash?index='+str(274541-j)
	page=requests.get(page)
	html = page.text

	page='https://explorer.nebl.io/api/getblock?hash='+html
	page=requests.get(page)
	html = page.text
	i=html.find('"mint"')
	html=html[i+7:]
	i=html.find(',')
	reward=float(html[:i])

	i = html.find('"tx":')
	html=html[i:-1]

	i = html.find(',')
	html=html[i+2:-1]
	i = html.find('"')
	txhash=html[:i]
	
	page='https://explorer.nebl.io/api/getrawtransaction?txid='+txhash+'&decrypt=1'
	page=requests.get(page)
	html = page.text

	i = html.find('"addresses":')
	miner=html[i+14:-1]
	i=miner.find('"')
	miner=miner[:i]
	
	print(j)

	if miner not in miners:
		miners.append(miner)
		stats.append(reward)
	else:
		k=miners.index(miner)
		stats[k]=stats[k]+reward
	if j%100==0:
		sleep(360)
	
		
print(miners)
print (stats)