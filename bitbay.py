import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib.request
import urllib.parse

record = {}
f_w=open("bitbay.txt",'w')

for j in range(1000):
	
	i=1
	while i!=-1:
		page='https://chainz.cryptoid.info/bay/api.dws?q=getblockhash&height='+str(1860000-j)
		page=requests.get(page)
		html = page.text
		i=html.find('wait 5')
		if i!=-1:
			sleep(360)
	
	i=1
	while i!=-1:
		html=html[1:-1]
		page='https://chainz.cryptoid.info/explorer/block.txs.dws?coin=bay&h='+html+'.js'
		page=requests.get(page)
		html = page.text
		if i!=-1:
			sleep(360)
			
	i = html.find('[{"a":')
	html = html[i+7:-1]

	i1 = html.find(',"v":')
	key = html[0:i1-1]
	f_w.write(key+' , ')
	
	if key in record:
		record[key] += 1
	else:
		record[key] = 1

for key in record:
	print(key)

for key in record:
	print(record[key])