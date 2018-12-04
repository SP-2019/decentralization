import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib
import math

miners=[]
stats=[]
height=10000000
f_w=open("lisk.txt",'w')
extra=0

for j in range(5000):
	page='https://explorer.lisk.io/api/getLastBlocks?n='+str((j+extra)*20)
	page=requests.get(page)
	html = page.text
	h1=html.find('"height":')
	h2=html.find(',"delegate"')
	
	while (height<=int(html[h1+9:h2])):
		html = html[h2:-1]
		h1=html.find('"height":')
		h2=html.find(',"delegate"')
		if h1==-1:
			extra=extra+1
			page='https://explorer.lisk.io/api/getLastBlocks?n='+str((j+extra)*20)
			page=requests.get(page)
			html = page.text
			h1=html.find('"height":')
			h2=html.find(',"delegate"')
	
	height=int(html[h1+len('"height":'):h2])
	i = html.find('"username":"')
	i2=html.find('","vote"')
	
	while (i!=-1):
		miner=html[i+12:i2]
		html=html[i2+8:]
		f_w.write(miner+' , ')
		if miner not in miners:
			miners.append(miner)
			stats.append(1)
		else:
			k=miners.index(miner)
			stats[k]=stats[k]+1
		i = html.find('"username":"')
		i2=html.find('","vote"')
	print(j)	
	
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