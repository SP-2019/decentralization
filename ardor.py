import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib.request
import urllib.parse
import json
from pprint import pprint

miners=[]
stats=[]

record = {}

for i in range(100):
	page='https://ardor.tools/ardor/nxt?requestType=getBlocks&firstIndex='+ str(100*i) + '&lastIndex=' + str(100*(i+1))
	page=requests.get(page)
	html = page.text
	data = json.loads(html)

	for j in range(100):
		key = data["blocks"][j]["generatorRS"]
		if key in record:
			record[key] += 1
		else:
			record[key] = 1
	print(i)
for key in record:
	print(key)

for key in record:
	print(record[key])