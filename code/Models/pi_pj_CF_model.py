'''
Written by : Saurabh Uttam, 20122055
			 Sujay Kumar, 20124006
'''
import csv
import math
from sets import Set
import operator
data_reader=csv.reader(open('../dataset/test/preprocess_data_new.csv','rt'))
market_basket={} #this will store the market basket for customers
row_count=0
for row in data_reader:
	if row_count==500:
		break
	market_basket[row[0]]=[row[1].split(',')+row[2].split(','),row[3].split(',')]
	row_count+=1
#print market_basket['161517']
#exit()
rating_reader=csv.reader(open('../dataset/test/trimed_rating_1000.csv','rt'))
rating={} #this will store the rating of user for items
count=0
for row in rating_reader:
	rating[row[0]+' '+row[1]]=float(row[2])
	#print row[0],row[1]
#	count+=1
	#if count==10:
	#	break
#exit()

product_popularity=csv.reader(open('./../dataset/output/update_pop.csv'))
popularity={}
for pro in product_popularity:
	popularity[pro[0]]=pro[1]

#this will calcualte the cosine similarity between twoc customers
def cosine_similarity(u1,u2):
	user1=list(Set(market_basket[u1][0]))
	user2=list(Set(market_basket[u2][0]))
	user1=sorted(user1)
	user2=sorted(user2)
	rating_sum=0
	i,j=0,0
	mod1=0
	mod2=0
	while i<len(user1) and j<len(user2):

		pid1=user1[i]
		'''if u1=='100401' and pid1=='1266857':
			print "heeellerlere"'''
		pid2=user2[j]
		try:
			mod1+=rating[u1+' '+pid1]**2
			#print "HEllo"
		except KeyError:
			i+=1
			continue
		try:
			mod2+=rating[u2+' '+pid2]**2
			#print "HEllo2"
		except KeyError:
			j+=1
			continue
		if pid1==pid2:
			rating_sum+=rating[u1+' '+pid1]*rating[u2+' '+pid2]
			i+=1
			j+=1
		elif pid1>pid2:
			j+=1
		else:
			i+=1
	try:
		return float(rating_sum)/(math.sqrt(mod1)*math.sqrt(mod2))
	except ZeroDivisionError:
		return 0

#this will return top 10 similar custormer
def top_rating_CF(u1):
	similarity={}
	for user in market_basket:
		if user==u1:
			continue
		similarity[user]=cosine_similarity(u1,user)
	sorted_similarity=sorted(similarity.items(),key=operator.itemgetter(1),reverse=True)
	return sorted_similarity

print "Calulating.."
true_count=0
total=0
for userID in market_basket:
	items=top_rating_CF(userID)
	count=0
	top_users={}
	for x,y in items:
		if count==9:
			break
		top_users[x]=y
		count+=1
	top_users[userID]=1

	print total

	users_item=[]
	for x in top_users:
		users_item.extend(market_basket[x][0])
	current_user_items=market_basket[userID][0]
	users_item=list(Set(users_item))

	product_rating={}
	S=0
	for item in users_item:
		temp=0.0
		count=0
		for user in top_users:
			try:
				temp_rating=rating[user+' '+item]
				count+=1
			except KeyError:
				continue
			temp+=float(temp_rating)*float(top_users[user])
		try:	
			product_rating[item]=(temp/count)*float(popularity[item])
		except ZeroDivisionError:
			continue
	count=0
	section_C=market_basket[userID][1]
	product_rating=sorted(product_rating.items(),key=operator.itemgetter(1),reverse=True)
	for x,y in product_rating:
		if count==10:
			break
		if x in section_C:
			true_count+=1
			break
		count+=1
	total+=1


print "accuracy: ",float(true_count)/total
