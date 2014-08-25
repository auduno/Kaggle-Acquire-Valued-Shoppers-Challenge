# -*- coding: UTF-8 -*-
import string, os
import numpy as np
from collections import defaultdict
from datetime import datetime, date

testset = False

offers_file = "../data/offers.csv"
transactions_file = "../data/transactions.csv"
if testset:
	history_file = "../data/testHistory.csv"
else:
	history_file = "../data/trainHistory.csv"

# will be created
reduced_file = "../data/reduced.csv" 
if testset:
	folder = "./test/"
else:
	folder = "./train/"
out_file = os.path.join(folder, "base_features.csv")

feature_list = ["offer_id", "never_bought_company", "never_bought_category", "never_bought_brand", \
	"has_bought_brand_company_category", "has_bought_brand_category", "has_bought_brand_company", \
	"offer_value", "total_spend_all", "total_spend_ccb", "has_bought_company", "has_bought_company_q", "has_bought_company_a", \
	"has_bought_company_30", "has_bought_company_q_30", "has_bought_company_a_30", "has_bought_company_60", \
	"has_bought_company_q_60", "has_bought_company_a_60", "has_bought_company_90", "has_bought_company_q_90", \
	"has_bought_company_a_90", "has_bought_company_180", "has_bought_company_q_180", "has_bought_company_a_180", \
	"has_bought_category", "has_bought_category_q", "has_bought_category_a", "has_bought_category_30", \
	"has_bought_category_q_30", "has_bought_category_a_30", "has_bought_category_60", "has_bought_category_q_60", \
	"has_bought_category_a_60", "has_bought_category_90", "has_bought_category_q_90", "has_bought_category_a_90", \
	"has_bought_category_180", "has_bought_category_q_180", "has_bought_category_a_180", "has_bought_brand", \
	"has_bought_brand_q", "has_bought_brand_a", "has_bought_brand_30", "has_bought_brand_q_30", "has_bought_brand_a_30", \
	"has_bought_brand_60", "has_bought_brand_q_60", "has_bought_brand_a_60", "has_bought_brand_90", "has_bought_brand_q_90", \
	"has_bought_brand_a_90", "has_bought_brand_180", "has_bought_brand_q_180", "has_bought_brand_a_180"]

def reduce_data(offers_file, transactions_file, reduced_file):
	start = datetime.now()
	#get all categories and comps on offer in a dict
	offers_cat = {}
	offers_co = {}
	for e, line in enumerate( open(offers_file) ):
		offers_cat[ line.split(",")[1] ] = 1
		offers_co[ line.split(",")[3] ] = 1
	#open output file
	with open(reduced_file, "wb") as outfile:
		#go through transactions file and reduce
		reduced = 0
		for e, line in enumerate( open(transactions_file) ):
			if e == 0:
				outfile.write( line ) #print header
			else:
				#only write when if category in offers dict
				if line.split(",")[3] in offers_cat or line.split(",")[4] in offers_co:
					outfile.write( line )
					reduced += 1
			#progress
			if e % 5000000 == 0:
				print e, reduced, datetime.now() - start
	print e, reduced, datetime.now() - start

def diff_days(s1,s2):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	b = datetime.strptime(s2, date_format)
	delta = b - a
	return delta.days

def generate_features(transactions_file, out_file):
	#keep a dictionary with the offerdata
	offers = {}
	offers_categories = {}
	offers_companies = {}
	for e, line in enumerate( open(offers_file) ):
		row = line.strip().split(",")
		offers[ row[0] ] = row
		offers_categories[row[1]] = 1
		offers_companies[row[3]] = 1

	# dicts with variables from history
	ids = {}
	for e, line in enumerate( open(history_file) ):
		if e > 0:
			row = line.strip().split(",")
			ids[row[0]] = row

	seen_ids = set([])

	outfile = open(out_file, "wb")
	outfile.write("label repeattrips id "+string.join(feature_list)+" market chain\n")
	
	#iterate through reduced dataset
	last_id = 0
	features = defaultdict(float)
	for e, line in enumerate( open(transactions_file) ):
		if e > 0: #skip header
			#poor man's csv reader
			row = line.strip().split(",")
			#write away the features when we get to a new shopper id
			if last_id != row[0] and e != 1:
				
				#generate negative features
				if "has_bought_company" not in features:
					features['never_bought_company'] = 1
				
				if "has_bought_category" not in features:
					features['never_bought_category'] = 1
					
				if "has_bought_brand" not in features:
					features['never_bought_brand'] = 1
					
				if "has_bought_brand" in features and "has_bought_category" in features and "has_bought_company" in features:
					features['has_bought_brand_company_category'] = 1
				
				if "has_bought_brand" in features and "has_bought_category" in features:
					features['has_bought_brand_category'] = 1
				
				if "has_bought_brand" in features and "has_bought_company" in features:
					features['has_bought_brand_company'] = 1
					
				outline = ""
				if not testset and last_id in ids:
					outline += str(features["label"]) + " " + ids[last_id][4] + " " + str(last_id)
				else:
					outline += "-1 -1 "+str(last_id)
				for l in feature_list:
					if l in features:
						outline += " "+str(features[l])
					else:
						outline += " 0"
				# write chain and market
				if last_id in ids:
					outline += " "+ids[last_id][3]
					outline += " "+ids[last_id][1]
				outline += "\n"
				if last_id in ids:
					outfile.write( outline )
					seen_ids.add(last_id)
				#reset features
				features = defaultdict(float)
			#check if we have a valid sample
			if row[0] in ids:
				#generate label and history
				history = ids[row[0]]
				if not testset and row[0] in ids:
					if ids[row[0]][5] == "t":
						features['label'] = 1
					else:
						features['label'] = 0
				
				features['offer_value'] = offers[ history[2] ][4]
				features['offer_id'] = history[2]
				
				offervalue = offers[ history[2] ][4]
				
				features['total_spend_all'] += float( row[10] )
				
				if row[3] in offers_categories or row[4] in offers_companies:
					features['total_spend_ccb'] += float( row[10] )
				
				if offers[ history[2] ][3] == row[4]:
					features['has_bought_company'] += 1.0
					features['has_bought_company_q'] += float( row[9] )
					features['has_bought_company_a'] += float( row[10] )
					
					date_diff_days = diff_days(row[6],history[-1])
					if date_diff_days < 30:
						features['has_bought_company_30'] += 1.0
						features['has_bought_company_q_30'] += float( row[9] )
						features['has_bought_company_a_30'] += float( row[10] )
					if date_diff_days < 60:
						features['has_bought_company_60'] += 1.0
						features['has_bought_company_q_60'] += float( row[9] )
						features['has_bought_company_a_60'] += float( row[10] )
					if date_diff_days < 90:
						features['has_bought_company_90'] += 1.0
						features['has_bought_company_q_90'] += float( row[9] )
						features['has_bought_company_a_90'] += float( row[10] )
					if date_diff_days < 180:
						features['has_bought_company_180'] += 1.0
						features['has_bought_company_q_180'] += float( row[9] )
						features['has_bought_company_a_180'] += float( row[10] )
				
				if offers[ history[2] ][1] == row[3]:
					
					features['has_bought_category'] += 1.0
					features['has_bought_category_q'] += float( row[9] )
					features['has_bought_category_a'] += float( row[10] )
					date_diff_days = diff_days(row[6],history[-1])
					if date_diff_days < 30:
						features['has_bought_category_30'] += 1.0
						features['has_bought_category_q_30'] += float( row[9] )
						features['has_bought_category_a_30'] += float( row[10] )
					if date_diff_days < 60:
						features['has_bought_category_60'] += 1.0
						features['has_bought_category_q_60'] += float( row[9] )
						features['has_bought_category_a_60'] += float( row[10] )
					if date_diff_days < 90:
						features['has_bought_category_90'] += 1.0
						features['has_bought_category_q_90'] += float( row[9] )
						features['has_bought_category_a_90'] += float( row[10] )						
					if date_diff_days < 180:
						features['has_bought_category_180'] += 1.0
						features['has_bought_category_q_180'] += float( row[9] )
						features['has_bought_category_a_180'] += float( row[10] )				
				if offers[ history[2] ][5] == row[5] and (row[3] in offers_categories or row[4] in offers_companies):
					features['has_bought_brand'] += 1.0
					features['has_bought_brand_q'] += float( row[9] )
					features['has_bought_brand_a'] += float( row[10] )
					date_diff_days = diff_days(row[6],history[-1])
					if date_diff_days < 30:
						features['has_bought_brand_30'] += 1.0
						features['has_bought_brand_q_30'] += float( row[9] )
						features['has_bought_brand_a_30'] += float( row[10] )
					if date_diff_days < 60:
						features['has_bought_brand_60'] += 1.0
						features['has_bought_brand_q_60'] += float( row[9] )
						features['has_bought_brand_a_60'] += float( row[10] )
					if date_diff_days < 90:
						features['has_bought_brand_90'] += 1.0
						features['has_bought_brand_q_90'] += float( row[9] )
						features['has_bought_brand_a_90'] += float( row[10] )						
					if date_diff_days < 180:
						features['has_bought_brand_180'] += 1.0
						features['has_bought_brand_q_180'] += float( row[9] )
						features['has_bought_brand_a_180'] += float( row[10] )	
			last_id = row[0]
			if e % 100000 == 0:
				print e
	# do stuff for ids without transactions
	allids = set(ids.keys())
	unseen_ids = allids.difference(seen_ids)
	for ui in unseen_ids:
		features = defaultdict(float)
		history = ids[ui]
		features['offer_value'] = offers[ history[2] ][4]
		features['offer_id'] = history[2]
		if not testset:
			if ids[ui][5] == "t":
				features['label'] = 1
			else:
				features['label'] = 0
		if "has_bought_company" not in features:
			features['never_bought_company'] = 1
		if "has_bought_category" not in features:
			features['never_bought_category'] = 1
		if "has_bought_brand" not in features:
			features['never_bought_brand'] = 1
		if "has_bought_brand" in features and "has_bought_category" in features and "has_bought_company" in features:
			features['has_bought_brand_company_category'] = 1
		if "has_bought_brand" in features and "has_bought_category" in features:
			features['has_bought_brand_category'] = 1
		if "has_bought_brand" in features and "has_bought_company" in features:
			features['has_bought_brand_company'] = 1
		outline = ""
		if not testset:
			outline += str(features["label"]) + " " + ids[ui][4] + " " + str(ui)
		else:
			outline += "-1 -1 "+str(ui)
		for l in feature_list:
			if l in features:
				outline += " "+str(features[l])
			else:
				outline += " 0"
		# write chain and market
		outline += " "+ids[ui][3]
		outline += " "+ids[ui][1]
		outline += "\n"
		outfile.write( outline )

if __name__ == '__main__':
	reduce_data(offers_file, transactions_file, reduced_file)
	generate_features(transactions_file, out_file)
