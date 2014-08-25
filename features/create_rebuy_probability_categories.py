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

# get categories we are interested in
categories = set([])
for e, line in enumerate( open("../data/offers.csv","r") ):
	if e > 0:
		li = line.strip().split(",")
		categories.add(li[1])
categories = list(categories)

of = open( os.path.join(folder, "category_repeat_buy_probability.csv"),"w")
of.write("category_id,cat_repeat_buy_prob_30d,cat_repeat_buy_prob_60d,cat_repeat_buy_prob_90d\n")

for c in categories:
	print "calculating repeat-probability for category "+c

	repeaters_30d = []
	repeaters_60d = []
	repeaters_90d = []

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
			# get all stuff
			for p in bought_pre_6m.keys():
				if p in firstbuy_date:
					if (user_dates[user]['lastdate']-firstbuy_date[p]).days > 30:
						repeat_within_30d = 0
						# check if it's repeated within thirty days
						for d in repeatbuy_dates[p]:
							if (d-firstbuy_date[p]).days < 30:
								repeat_within_30d = 1
						repeaters_30d.append(repeat_within_30d)
					if (user_dates[user]['lastdate']-firstbuy_date[p]).days > 60:
						repeat_within_60d = 0
						# check if it's repeated within thirty days
						for d in repeatbuy_dates[p]:
							if (d-firstbuy_date[p]).days < 60:
								repeat_within_60d = 1
						repeaters_60d.append(repeat_within_60d)
					if (user_dates[user]['lastdate']-firstbuy_date[p]).days > 90:
						repeat_within_90d = 0
						# check if it's repeated within thirty days
						for d in repeatbuy_dates[p]:
							if (d-firstbuy_date[p]).days < 90:
								repeat_within_90d = 1
						repeaters_90d.append(repeat_within_90d)

			# reset variables
			bought_pre_6m = defaultdict(bool)
			firstbuy_date = {}
			repeatbuy_dates = defaultdict(list)		
		user = li[0]
		category = li[3]
		product = string.join(li[3:6]," ")
		date = datetime.datetime.strptime(li[6],"%Y-%m-%d").date()
		if category == c and float(li[10]) >= 0 and user in user_dates:
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

	# write out probabilities
	rep_30 = float(np.sum(repeaters_30d))/float(len(repeaters_30d))
	rep_60 = float(np.sum(repeaters_60d))/float(len(repeaters_60d))
	rep_90 = float(np.sum(repeaters_90d))/float(len(repeaters_90d))
	print "done with "+c
	print "number items for 30d : "+str(len(repeaters_30d))
	print "rep30 : "+str(rep_30)
	print "rep60 : "+str(rep_60)
	print "rep90 : "+str(rep_90)
	of.write(c+","+str(rep_30)+","+str(rep_60)+","+str(rep_90)+"\n")
