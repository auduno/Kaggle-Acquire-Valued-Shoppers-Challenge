import datetime,string,os
import numpy as np
from collections import defaultdict

testset = False
if testset:
	folder = "./test/"
else:
	folder = "./train/"

# get start and enddate of all users
user_dates = {}
fi = open("../data/user_dates.csv","r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	user_dates[li[0]] = {'firstdate' : datetime.datetime.strptime(li[1],"%Y-%m-%d").date(),'lastdate' : datetime.datetime.strptime(li[2],"%Y-%m-%d").date() }

# get products we are interested in
productids = set([])
for e, line in enumerate( open("../data/offers.csv","r") ):
	if e > 0:
		li = line.strip().split(",")
		productids.add(li[1]+" "+li[3]+" "+li[5])
productids = list(productids)

of = open( os.path.join(folder, "product_repeat_buy_probability.csv"),"w")
of.write("product_id,repeat_buy_prob_30d,repeat_buy_prob_60d,repeat_buy_prob_90d\n")


repeaters_30d = defaultdict(list)
repeaters_60d = defaultdict(list)
repeaters_90d = defaultdict(list)

fi = open("../data/reduced.csv","r")
fi.next()
# set standard variables
bought_pre_6m = defaultdict(bool)
firstbuy_date = {}
repeatbuy_dates = defaultdict(list)
lastid = 0

for e,lines in enumerate(fi):
	li = lines.strip().split(",")
	if not lastid == li[0] and e > 0:
		# check if it's valid
		for pi in productids:
			if pi in firstbuy_date:
				if (user_dates[user]['lastdate']-firstbuy_date[pi]).days > 30:
					repeat_within_30d = 0
					# check if it's repeated within thirty days
					for d in repeatbuy_dates[pi]:
						if (d-firstbuy_date[pi]).days < 30:
							repeat_within_30d = 1
					repeaters_30d[pi].append(repeat_within_30d)
				if (user_dates[user]['lastdate']-firstbuy_date[pi]).days > 60:
					repeat_within_60d = 0
					# check if it's repeated within thirty days
					for d in repeatbuy_dates[pi]:
						if (d-firstbuy_date[pi]).days < 60:
							repeat_within_60d = 1
					repeaters_60d[pi].append(repeat_within_60d)
				if (user_dates[user]['lastdate']-firstbuy_date[pi]).days > 90:
					repeat_within_90d = 0
					# check if it's repeated within thirty days
					for d in repeatbuy_dates[pi]:
						if (d-firstbuy_date[pi]).days < 90:
							repeat_within_90d = 1
					repeaters_90d[pi].append(repeat_within_90d)

		# reset variables
		bought_pre_6m = defaultdict(bool)
		firstbuy_date = {}
		repeatbuy_dates = defaultdict(list)		
	user = li[0]
	product = string.join(li[3:6]," ")
	date = datetime.datetime.strptime(li[6],"%Y-%m-%d").date()
	if product in productids and float(li[10]) >= 0:
		if (date - user_dates[user]['firstdate']).days < 30*6:
			# register if user bought the product in first half of year
			bought_pre_6m[product] = True
		elif bought_pre_6m[product] == False:
			# candidate for calculation
			if not product in firstbuy_date:
				firstbuy_date[product] = date
			else:
				# append to dates
				repeatbuy_dates[product].append(date)
	lastid = li[0]
	if e % 1000000 == 0 and e > 0:
		print e

# get probabilities for categories (replace with this when count is below 100)
category_repbuy_dict = {}
fi = open(os.path.join(folder, "category_repeat_buy_probability.csv"),"r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	category_repbuy_dict[li[0]] = li[1:]

# write out probabilities
for pi in productids:
	rep_30 = float(np.sum(repeaters_30d[pi]))/float(len(repeaters_30d[pi]))
	rep_60 = float(np.sum(repeaters_60d[pi]))/float(len(repeaters_60d[pi]))
	rep_90 = float(np.sum(repeaters_90d[pi]))/float(len(repeaters_90d[pi]))
	if len(repeaters_30d[pi]) < 100:
		print "replacing product "+pi+" probs with category probs since number of examples is below 100 :"+str(len(repeaters_30d[pi]))
		cat = pi.split()[0]
		of.write(pi+","+string.join(category_repbuy_dict[cat],",")+"\n")
	else:
		print "product "+pi+" nums:"+str(len(repeaters_30d[pi]))
		of.write(pi+","+str(rep_30)+","+str(rep_60)+","+str(rep_90)+"\n")

