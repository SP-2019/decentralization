import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib.request
import urllib.parse


page=requests.get('https://explorer.qtum.org/insight-api/blocks')
html = page.text
i=html.find("minedBy")
miners=[]

while (i!=-1):
	miner=html[i+10:i+44]
	html=html[i+44:-1]

	if miner not in miners:
		print(len(re.findall(miner, html))+1)
	i=html.find("minedBy")
	miners.append(miner)
	
