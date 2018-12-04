import requests, json
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib
import math

miners=[]
stats=[]
f_w=open("wayki.txt",'w')

header={'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
'Connection': 'keep-alive',
'Content-Length': '36',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Cookie': 'Language=en; JSESSIONID=E810B19D18174AE662E43636DFF2EE06',
'DNT': '1',
'Host': 'www.waykiscan.com',
'Origin': 'https://www.waykiscan.com',
'Referer': 'https://www.waykiscan.com/block_blockcontentpage.do',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'}

for j in range(10000):
	page='https://www.waykiscan.com/info/trade/findTradesByPage.do?_csrf=36914bfc-b60e-4679-b29a-b8ba7a952b73'
	data_request={'btraconfbhight':790375-j, 'page': 1, 'rows': 15}
	page=requests.post(page, headers=header, data=data_request) 
	html = page.text
	
	type='0'
	while type!='1':
		i=html.find('btratype')
		html=html[i+10:]
		i=html.find(',')
		type=html[:i]
		
	i=html.find('btratoaddr')
	html=html[i+13:]
	i=html.find('"')
	miner=html[0:i]
	
	print(miner, j)
	f_w.write(miner+',')
	if miner not in miners:
		miners.append(miner)
		stats.append(1)
	else:
		k=miners.index(miner)
		stats[k]=stats[k]+1
	
	if j%10==0:
		sleep(5)

print(miners)
print (stats)	



stats.sort(reverse=True)
sum_stats=sum(stats)

for i in range(len(stats)):
	stats[i]=float(stats[i])/float(sum_stats)

sum_=0; num_3=0; num_5=0;
for i in range(len(stats)):
    sum_=sum_+stats[i]
    
    if (num_3==0) and (sum_>=0.333333333333333333):
        num_3=i 

    if (num_5==0) and (sum_>=0.5):
      num_5=i
      break

print(num_3,num_5)

entropy_3=0; entropy_5=0; entropy=0;
for i in range(num_3+1):
    entropy_3=entropy_3-stats[i]/(sum(stats[:num_3+1]))*math.log(stats[i]/sum(stats[:num_3+1]),2);

for i in range(num_5+1):
    entropy_5=entropy_5-stats[i]/(sum(stats[:num_5+1]))*math.log(stats[i]/sum(stats[:num_5+1]),2);
	
for i in range(len(stats)):
    entropy=entropy-stats[i]*math.log(stats[i],2);


A=0; B=0; C=0;
power_5=stats[:num_5+1]; power_3=stats[:num_3+1];

for i in range(len(stats)):
    for j in range(len(stats)):
        A=A+abs(stats[i]-stats[j])
        if (i<=num_5) and (j<=num_5):
            B=B+abs(stats[i]-stats[j])

        if (i<=num_3) and (j<=num_3):
            C=C+abs(stats[i]-stats[j])

Gini_100=A/2/len(stats)/sum(stats);
Gini_50=B/2/(num_5+1)/sum(stats[:num_5+1]);
Gini_30=C/2/(num_3+1)/sum(stats[:num_3+1]);


f_w.write("number="+str(len(stats))+"  gini="+str(Gini_100)+"  entropy="+str(entropy)+ \
"  number="+str(num_5+1)+"  gini="+str(Gini_50)+"  entropy="+str(entropy_5)+ \
"  number="+str(num_3+1)+"  gini="+str(Gini_30)+"  entropy="+str(entropy_3)+'\n')

f_w.close()					