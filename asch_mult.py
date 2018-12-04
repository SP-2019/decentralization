import requests, json
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib
import math

page='https://exnode.asch.io/api/delegates?orderBy=rate:asc&limit=100&offset=0'
page=requests.get(page)
html_a = page.text
cnt=0

while html_a.find('"name":"')!=-1:
	i=html_a.find('"name":"')
	html_a=html_a[i+len('"name":"'):]
	i=html_a.find('"')
	name=html_a[:i]
	page='https://exnode.asch.io/api/v2/misc/blocksForgedBy?orderBy=timestamp:desc&limit=10&offset=0&name='+name+'&reverse=1'
	page=requests.get(page)
	html = page.text
	i=html.find('height":')
	html=html[i+len('height":'):]
	i=html.find(',')
	height=html[:i]
	if int(height)>6600000:
		cnt=cnt+1
	print(name, height)
	
print(cnt)