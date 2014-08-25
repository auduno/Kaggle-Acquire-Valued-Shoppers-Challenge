from datetime import datetime, date
from collections import defaultdict
import numpy as np
import os, string

testset = False

def diff_days(s1,s2):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	b = datetime.strptime(s2, date_format)
	delta = b - a
	return delta.days

offers_file = "../data/offers.csv"
transactions_file = "../data/transactions.csv"
if testset:
	history_file = "../data/testHistory.csv"
	folder = "./test/"
else:
	history_file = "../data/trainHistory.csv"
	folder = "./train/"
out_file = os.path.join(folder, "user_features.csv")

def generate_features(history_file, transactions_file, out_file):
	#keep a dictionary with the offerdata
	offers = {}
	for e, line in enumerate( open(offers_file) ):
		row = line.strip().split(",")
		offers[ row[0] ] = row

	#keep two dictionaries with the shopper id's from train
	ids = {}
	for e, line in enumerate( open(history_file) ):
		if e > 0:
			row = line.strip().split(",")
			ids[row[0]] = row
	
	#get category-dept map
	cat_dept = {}
	dept_cat = {}
	for e, line in enumerate( open("../data/cat_dept_map.csv","r") ):
		row = line.strip().split(",")
		cat_dept[row[0]] = row[1]
		if not row[1] in dept_cat:
			dept_cat[row[1]] = []
		dept_cat[row[1]].append(row[0])

	seen_ids = set([])
	out_train = open(out_file, "wb")
	feature_list = ["total_spend_30","dep_spend_30","dep_count_30","visits_30","prodid_spend_30","prodid_count_30","prodid_spend_all","prodid_count_all","prodid_spend_corr"]
	out_train.write("id," + string.join(feature_list,",")+"\n")

	# get product marketshares for correcting prodid_spend
	product_marketshares = {}
	fi = open( os.path.join(folder, "product_features.csv"),"r")
	fi.next()
	for lines in fi:
		li = lines.strip().split(",")
		product_marketshares[li[0]] = float(li[1])

	#iterate through dataset
	last_id = 0
	features = defaultdict(float)
	days = [0]*30
	filt = open(transactions_file, "r")
	filt.next()
	for e, line in enumerate( filt ):
		#poor man's csv reader
		row = line.strip().split(",")
		#write away the features when we get to a new shopper id
		if last_id != row[0] and e != 0:
			if last_id in ids:
				features['visits_30'] = np.sum(days)
				
				outline = str(last_id)
				for l in feature_list:
					if l == "prodid_spend_corr" and not l in features:
						prodid = offers[history[2]][1]+" "+offers[history[2]][3]+" "+offers[history[2]][5]
						outline += ",-"+str(100*product_marketshares[prodid])
					elif l in features:
						outline += ","+str(features[l])
					else:
						outline += ",0"
				
				outline += "\n"
				
				out_train.write( outline )
				seen_ids.add(last_id)

			# reset features
			features = defaultdict(float)
			days = [0]*30
			
		#generate features from transaction record
		if row[0] in ids:
			history = ids[row[0]]

			dep = cat_dept[offers[ history[2] ][1]]
			cats = dept_cat[dep]
			
			date_diff_days = diff_days(row[6],history[-1])
			# get total spend last 30 days
			if date_diff_days < 30:
				features['total_spend_30'] += float( row[10] )
			
			# check how many bought this exact item over last 30 days
			if offers[history[2]][3] == row[4] and offers[ history[2] ][1] == row[3] and offers[ history[2] ][5] == row[5]:
				if date_diff_days < 30:
					features['prodid_spend_30'] += float(row[10])
					features['prodid_count_30'] += float(row[9])
				features['prodid_spend_all'] += float(row[10])
				features['prodid_spend_corr'] += float(row[10])
				features['prodid_count_all'] += float(row[9])
			
			# check if this category is in the dept
			if row[3] in cats:
				if date_diff_days < 30:
					features['dep_count_30'] += float( row[9] )
					features['dep_spend_30'] += float( row[10] )
			
			# append this day to list of last 30 days
			if date_diff_days < 30:
				days[date_diff_days] = 1

		last_id = row[0]
		if e % 100000 == 0 and e > 0:
			print e

	# write out the last entry
	if last_id in ids:
		features['visits_30'] = np.sum(days)
		
		outline = str(last_id)
		for l in feature_list:
			if l == "prodid_spend_corr" and not l in features:
				prodid = offers[history[2]][1]+" "+offers[history[2]][3]+" "+offers[history[2]][5]
				outline += ",-"+str(100*product_marketshares[prodid])
			elif l in features:
				outline += ","+str(features[l])
			else:
				outline += ",0"
		
		outline += "\n"
		
		out_train.write( outline )
		seen_ids.add(last_id)

	# do stuff for ids without transactions
	allids = set(ids.keys())
	unseen_ids = allids.difference(seen_ids)
	if len(unseen_ids) > 0:
		import pdb;pdb.set_trace()
	for ui in unseen_ids:
		outline = str(ui)
		outline += "0,0,0,0,0,0,0,0\n"
		out_train.write( outline )

generate_features(history_file, transactions_file, out_file)