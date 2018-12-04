from selenium import webdriver
import math

driver = webdriver.Chrome(executable_path=r'C:/Users/yujin_k/Downloads/chromedriver_win32/chromedriver.exe')
driver.implicitly_wait(3)

driver.get('http://blockchain.prizm.space/index.html')

miners=[]
stats=[]

height2=10000000
for j in range(100):
	driver.get('http://blockchain.prizm.space/prizm?requestType=getBlocks&firstIndex='+str(j*100)+'&lastIndex='+str((j+1)*100)+'&random=0.33603418870351387')

	html = driver.page_source
	
	while html.find('generatorRS":"')!=-1:
		i=html.find('generatorRS":"')
		html=html[i+len('generatorRS":"'):]
		i=html.find('"')
		miner=html[:i]
		
		i=html.find('"height":')
		html=html[i+len('"height":'):]
		i=html.find(',')
		height=int(html[:i])
		
		if height<height2:
			height2=height
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

entropy_3=0; entropy_5=0; entropy=0;

for i in range(num_3+1):
    entropy_3=entropy_3-stats[i]/(sum(stats[:num_3+1]))*math.log(stats[i]/sum(stats[:num_3+1]),2);

for i in range(num_5+1):
    entropy_5=entropy_5-stats[i]/(sum(stats[:num_5+1]))*math.log(stats[i]/sum(stats[:num_5+1]),2);
	
for i in range(len(stats)):
    entropy=entropy-stats[i]*math.log(stats[i],2);


A=0; B=0; C=0;
power_5=stats[:num_5]; power_3=stats[:num_3];

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


print("number="+str(len(stats))+"  gini="+str(Gini_100)+"  entropy="+str(entropy)+ \
"  number="+str(num_5+1)+"  gini="+str(Gini_50)+"  entropy="+str(entropy_5)+ \
"  number="+str(num_3+1)+"  gini="+str(Gini_30)+"  entropy="+str(entropy_3))
