import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib
import json
from pprint import pprint

record = {}
count = 0
f_w=open("cryptonex.txt",'w')

for i in range(1000): 
	link = 'https://explorer.cryptonex.org/api/getblockhash?index=' + str(607000-i)
	hash = requests.get(link).text
	link = 'https://explorer.cryptonex.org/api/getblock?hash=' + str(hash)
	block = requests.get(link).text
	data = json.loads(block)
	if len(data["tx"]) != 2:
		print(len(data["tx"]))
		continue
	tx = data["tx"][1]
	link = 'https://explorer.cryptonex.org/api/getrawtransaction?txid=' + tx + '&decrypt=1'
	tx = requests.get(link).text
	# print(tx)
	# data = json.loads(tx)
	j = tx.find("addresses")
	key = tx[j+13 : j+47]
	f_w.write(key+' , ')
	
	if key in record:
		record[key] += 1
	else:
		record[key] = 1
	count += 1

	print(i)

for key in record:
	print(key)

for key in record:
	print(record[key])