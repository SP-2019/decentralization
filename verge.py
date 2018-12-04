import requests, json
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib
import math


miners=[]
stats=[]
f_w=open("verge.txt",'w')

for j in range(10000):
	page='https://prohashing.com/explorerJson/getBlockByHeight?coin_id=146&height='+str(2582755-j)
	page=requests.get(page) 
	html = page.text
	bxhash=html[9:-2]

	page='https://prohashing.com/explorerJson/getBlock?coin_id=146&hash='+bxhash
	page=requests.get(page)
	html = page.text
	
	i=html.find('"tx":')
	html=html[i:-1]
	
	check='false'
	while check=='false':
		i=html.find('"hash"')
		html=html[i+8:]
		i=html.find('"')
		txhash=html[0:i]
		i=html.find('"coinbase"')
		html=html[i+11:]
		i=html.find('}')
		check=html[0:i]
	
	page='https://prohashing.com/explorerJson/getTransaction?coin_id=146&transaction_id='+txhash
	page=requests.get(page)
	html=page.text
	i=0
	cnt=0
	while i!=-1:
		i=html.find('"address":')
		html=html[i+11:]
		i=html.find('"')
		if cnt==0:
			miner=html[:i]
		else:
			miner='&'+miner
		i=html.find('"address":')
	
	f_w.write(miner+' , ')
	print(j)
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

exit()

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