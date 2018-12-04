import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib.request
import urllib.parse

page='https://coinmarketcap.com/coins/'
page=requests.get(page)
html = page.text
i=0
i=html.find('currency-name"')
while i!=-1:
	html=html[i+len('currency-name" data-sort="'):]
	i=html.find('"')
	name=html[:i]
	i=html.find('currency-name"')
	print(name)