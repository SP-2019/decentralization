import requests, json
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib
import math


miners=[]
stats=[]
f_w=open("ltc.txt",'w')

for j in range(10000):
	
	page='https://chainz.cryptoid.info/ltc/api.dws?q=getblockhash&height='+str(1510180-j)
	page=requests.get(page)
	html = page.text
	while html.find('wait 5')!=-1:
		sleep(360)
		page='https://chainz.cryptoid.info/ltc/api.dws?q=getblockhash&height='+str(1510180-j)
		page=requests.get(page)
		html = page.text
	bxhash=html[1:-1]
	
	i=0
	while i!=-1:
		page='https://chainz.cryptoid.info/ltc/block.dws?'+bxhash
		page=requests.get(page)
		html = page.text
		if html.find('wait 5')!=-1:
			sleep(360)
		i=html.find('wait 5')
		
	if html.find("extracted by")!=-1:
		i=html.find("extracted by")
		html=html[i:]
		i=html.find('>')
		html=html[i+1:]
		i=html.find('<')
		miner=html[:i]
	else:
		i=0
		while i!=-1:
			page='https://chainz.cryptoid.info/explorer/block.txs.dws?coin=ltc&h='+bxhash+'.js'
			page=requests.get(page)
			html = page.text
			if html.find('wait 5')!=-1:
				sleep(360)
			else:
				value=0
				while value<=0:
					i=html.find('"a":"')
					html=html[i+len('"a":"'):]
					i=html.find('"')
					miner=html[:i]
					i=html.find('"v":')
					html=html[i+len('"v":'):]
					i=html.find('}')
					value=float(html[:i])
				
			
			i=html.find('wait 5')
		
	print(miner, j)
	if miner not in miners:
		miners.append(miner)
		stats.append(1)
	else:
		k=miners.index(miner)
		stats[k]=stats[k]+1
	
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