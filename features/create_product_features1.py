import string, os
from datetime import datetime, date
from collections import defaultdict
import numpy as np

testset = False
if testset:
	folder = "./test/"
else:
	folder = "./train/"

offers_file = "../data/offers.csv"
transactions_file = "../data/transactions.csv"

def generate_features(transactions_file):
	# get the productids we are interested in
	# get all the categories we are interested in
	productids = set([])
	categories = set([])
	departments = set([])
	for e, line in enumerate( open(offers_file) ):
		if e > 0:
			li = line.strip().split(",")
			categories.add(li[1])
			departments.add(li[1][:-2])
			productids.add(li[1]+" "+li[3]+" "+li[5])
	categories = list(categories)
	productids = list(productids)
	departments = list(departments)


	usercount = 0
	productcounts = defaultdict(int)
	categorycounts = defaultdict(int)
	departmentcounts = defaultdict(int)

	mshare_product = defaultdict(int)
	category_bought = defaultdict(int)
	department_bought = defaultdict(int)

	prod_spend_all = defaultdict(float)
	cat_spend_all = defaultdict(float)
	dep_spend_all = defaultdict(float)
	
	product_bought_dict = defaultdict(int)
	category_bought_dict = defaultdict(int)
	department_bought_dict = defaultdict(int)
	
	prod_spend = defaultdict(int)
	cat_spend = defaultdict(int)
	dep_spend = defaultdict(int)
	
	prod_unit_price = {}
	for pi in productids:
		prod_unit_price[pi] = {}

	# for each user
		# count how many different productids she buys in each category (keep dict of categories, with entry "count", and "sum"(added to as we go))
		# count whether they bought the productid (simple dict of productid with entry "count")
		# count whether they bought the category (simple dict of category with entry "count")
		# count how many users (simple counter)
	# keep count of how many different products there are in each category (i.e. a dict with counts)

	# calculate popularity of "our" productids in category (i.e. marketshare) (simple count of buys in category, simple count of productids)
	# calculate product popularity
	# calculate category popularity
	# calculate on average how many *different* products each user buys in each category (if they buy in that category?)

	allspend = 0.0

	#iterate through dataset
	last_id = 0
	features = defaultdict(float)
	filt = open(transactions_file, "r")
	filt.next()
	for e, line in enumerate( filt ):
		#poor man's csv reader
		li = line.strip().split(",")

		#write away the features when we get to a new shopper id
		if last_id != li[0] and e != 0:
			usercount += 1
			for pi in productids:
				productcounts[pi] += product_bought_dict[pi]
				prod_spend_all[pi] += (prod_spend[pi]/allspend)
			for c in categories:
				categorycounts[c] += category_bought_dict[c]
				cat_spend_all[c] += (cat_spend[c]/allspend)
			for d in departments:
				departmentcounts[d] += department_bought_dict[d]
				dep_spend_all[d] += (dep_spend[d]/allspend)

			# reset features
			product_bought_dict = defaultdict(int)
			category_bought_dict = defaultdict(int)
			department_bought_dict = defaultdict(int)
			prod_spend = defaultdict(int)
			cat_spend = defaultdict(int)
			dep_spend = defaultdict(int)
		
		allspend += float(li[10])

		prodid = string.join(li[3:6]," ")
		if prodid in productids:
			product_bought_dict[prodid] = 1
			mshare_product[prodid] += 1
			prod_spend[prodid] += float(li[10])
			unit = li[7]+" "+li[8]
			if not unit in prod_unit_price[prodid]:
				prod_unit_price[prodid][unit] = {'count' : 0, 'sum_price' : 0.}
			if int(li[9]) > 0 and float(li[10]) > 0.0:
				prod_unit_price[prodid][unit]['count'] += int(li[9])
				prod_unit_price[prodid][unit]['sum_price'] += float(li[10])

		if li[3] in categories:
			category_bought_dict[li[3]] = 1
			category_bought[li[3]] += 1
			cat_spend[li[3]] += float(li[10])

		if li[3][:-2] in departments:
			department_bought_dict[li[3][:-2]] = 1
			department_bought[li[3][:-2]] += 1
			dep_spend[li[3][:-2]] += float(li[10])

		last_id = li[0]
		if e % 1000000 == 0 and e > 0:
			print e

	# write out productfile 
	of = open( os.path.join(folder, "product_features.csv") ,"w")
	of.write("productid,marketshare_in_cat,share_of_cust_bought_prod,share_prod_spend,share_of_cust_bought_cat,"+\
		"share_cat_spend,avg_price_per_cheapest_common_unit,avg_price_per_most_common_unit,marketshare_in_dep,share_of_cust_bought_dep,share_dep_spend\n")
	for pi in productids:
		of.write(pi)
		of.write(","+str( float(mshare_product[pi])/float(category_bought[pi.split()[0]]) ) )
		of.write(","+str( float(productcounts[pi])/float(usercount) ) )
		of.write(","+str( prod_spend_all[pi]/float(usercount) ) )
		of.write(","+str( float(categorycounts[pi.split()[0]])/float(usercount) ) )
		of.write(","+str( cat_spend_all[pi.split()[0]]/float(usercount) ) )
		# find the average price of the cheapest unit (that more 10% buys) and average price of the most common unit
		min_unit_price = 100000000000000.0
		max_unit_count = 0
		max_unit_count_price = 0.0
		total_units = np.sum([u['count'] for u in prod_unit_price[pi].values()])
		for u in prod_unit_price[pi].values():
			price = float(u['sum_price'])/float(u['count'])
			if float(u['count'])/float(total_units) > 0.10 and price < min_unit_price:
				min_unit_price = price
			if u['count'] > max_unit_count:
				max_unit_count = u['count']
				max_unit_count_price = price
		if min_unit_price == 100000000000000.0:
			min_unit_price = max_unit_count_price
		
		of.write(","+str(min_unit_price) )
		of.write(","+str(max_unit_count_price) )

		of.write(","+str( float(mshare_product[pi])/float(department_bought[pi.split()[0][:-2]]) ) )
		of.write(","+str( float(departmentcounts[pi.split()[0][:-2]])/float(usercount) ) )
		of.write(","+str( dep_spend_all[pi.split()[0][:-2]]/float(usercount) ) )


		of.write("\n")
	of.close()

generate_features(transactions_file)