import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib.request
import urllib.parse
import json
from pprint import pprint

record = {}
count = 0
f_w=open("white.txt",'w')

for i in range(1500): 
	link = 'http://explorer2.whitecoin.info/api/getblockhash?index=' + str(786000-i)
	hash = requests.get(link).text	
	link = 'http://explorer2.whitecoin.info/api/getblock?hash=' + str(hash)
	block = requests.get(link).text
	data = json.loads(block)
	if len(data["tx"]) != 2:
		print(len(data["tx"]))
		continue

	tx = data["tx"][1]
	link = 'http://explorer2.whitecoin.info/api/getrawtransaction?txid=' + tx + '&decrypt=1'
	tx = requests.get(link).text
	# print(tx)
	# data = json.loads(tx)
	j = tx.find("addresses")
	key = tx[j+25 : j+59]
	f_w.write(key+' , ')
	if key in record:
		record[key] += 1
	else:
		record[key] = 1
	count += 1

print(count)

for key in record:
	print(key)

for key in record:
	print(record[key])