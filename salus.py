import requests
import re
from bs4 import BeautifulSoup as bs
from time import sleep
import urllib
import math

record = {}
rewards= {}
f_w=open("salus.txt",'w')

for j in range(10000):
	link = 'http://www.presstab.pw/phpexplorer/SLS/block.php?height='+str(182389-j)
	page = requests.get(link)
	html = page.text
	i = html.find('Tx 1 Hash:')
	html = html[i+38 : -1]
	i = html.find('>')
	tx = html[0:i]
	link = 'http://www.presstab.pw/phpexplorer/SLS/tx.php?tx='+tx
	page = requests.get(link)
	html = page.text
	i = html.find('sent to <a href=address.php?address=')
	html = html[i+len('sent to <a href=address.php?address=') : -1]
	i = html.find('>')
	addr = html[0:i]
	i=html.find('Total Fee')
	html=html[i+len('Total Fee</th><td>-'):]
	i=html.find('<')
	reward=float(html[:i])
		
	if addr in record:
		record[addr] += reward
		rewards[addr]+=1
	else:
		record[addr] = reward
		rewards[addr]=1
	print(j)
		
for addr in record:
	print(addr)

for addr in record:
	print(record[addr])

for addr in record:
	print(rewards[addr])	

stats=rewards

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
Gini_50=B/2/num_5/sum(stats[:num_5+1]);
Gini_30=C/2/num_3/sum(stats[:num_3+1]);


f_w.write("number="+str(len(stats))+"  gini="+str(Gini_100)+"  entropy="+str(entropy)+ \
"  number="+str(num_5+1)+"  gini="+str(Gini_50)+"  entropy="+str(entropy_5)+ \
"  number="+str(num_3+1)+"  gini="+str(Gini_30)+"  entropy="+str(entropy_3)+'\n')

f_w.close()					