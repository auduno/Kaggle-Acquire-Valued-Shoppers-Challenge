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

# get the products and categories we are interested in
productids = set([])
categories = set([])
for e, line in enumerate( open(offers_file) ):
	if e > 0:
		li = line.strip().split(",")
		categories.add(li[1])
		productids.add(li[1]+" "+li[3]+" "+li[5])
categories = list(categories)
productids = list(productids)

category_product_unit_prices = {}
for c in categories:
	category_product_unit_prices[c] = {}

filt = open(transactions_file, "r")
filt.next()
for e, line in enumerate( filt ):
	li = line.strip().split(",")
	category = li[3]
	if category in categories:
		prodid = string.join(li[3:6]," ")
		unit = string.join(li[7:9]," ")
		if not prodid in category_product_unit_prices[category]:
			category_product_unit_prices[category][prodid] = {}
		if not unit in category_product_unit_prices[category][prodid]:
			category_product_unit_prices[category][prodid][unit] = []
		if float(li[10]) > 0:
			category_product_unit_prices[category][prodid][unit].append(float(li[10]))
	if e % 10000000 == 0 and e > 0:
		print e

product_features = {}

product_comparisons = {
	'4401 105100050 13791' : {'product_container' : '19.6 OZ', 'category_container' : '19 OZ'},
	'5824 105190050 26456' : {'product_container' : '13 OZ', 'category_container' : '13 OZ'},
	'4517 105450050 1322' : {'product_container' : '18 OZ', 'category_container' : '18 OZ'}, # also maybe use categories with '16 OZ'
	'1726 104460040 7668' : {'product_container' : '35 CT', 'category_container' : '35 CT'},
	'9909 1089520383 28840' : {'product_container' : '5 OZ', 'category_container' : '5 OZ'},
	'5619 107717272 102504' : {'product_container' : '8 OZ', 'category_container' : '8 OZ'},
	'3509 103320030 875' : {'product_container' : '50 OZ', 'category_container' : '50 OZ'},
	'2119 108079383 6926' : {'product_container' : '144 OZ', 'category_container' : '144 OZ'},
	'9909 107127979 6732' : {'product_container' : '12 OZ', 'category_container' : '12 OZ'},
	'7205 103700030 4294' : {'product_container' : '5.8 OZ', 'category_container' : '5.8 OZ'},
	'6202 1087744888 64486' : {'product_container' : '8.8 OZ', 'category_container' : '9 OZ'},
	'5558 107120272 5072' : {'product_container' : '9.3 OZ', 'category_container' : '9 OZ'},
	'3504 104460040 7668' : {'product_container' : '22 OZ', 'category_container' : '20 OZ'},
	'5122 107106878 17311' : {'product_container' : '42.72 OZ', 'category_container' : '42.72 OZ'},
	'9115 108500080 93904' : {'product_container' : '0.75 LT', 'category_container' : '0.75 LT'},
	'2202 104460040 3718' : {'product_container' : '32 OZ', 'category_container' : '30.3 OZ'},
	'1703 104460040 7668' : {'product_container' : '32 OZ', 'category_container' : '32 OZ'},
	'706 104127141 26189' : {'product_container' : '64 OZ', 'category_container' : '64 OZ'},
	'3203 106414464 13474' : {'product_container' : '5 OZ', 'category_container' : '5 OZ'},
	'799 1076211171 17286' : {'product_container' : '12 OZ', 'category_container' : '12.7 OZ'},
	'5616 104610040 15889' : {'product_container' : '8 OZ', 'category_container' : '8 OZ'},
}

#conts = defaultdict(list)
#[[conts.__setitem__(k, conts.__getitem__(k) + category_product_unit_prices['2202'][p][k]) for k in category_product_unit_prices['2202'][p]] for p in pids]

for pr in productids:
	
	category = pr.split()[0]
	catdict = category_product_unit_prices[category]
	
	category_container = product_comparisons[pr]['category_container']
	product_container = product_comparisons[pr]['product_container']

	prices = []
	for prod,val in catdict.iteritems():
		if not prod == pr:
			if category_container in val:
				prices = prices + val[category_container]

	product_prices = catdict[pr][product_container]

	if not category_container == product_container:
		cat_size = float(category_container.split()[0])
		prod_size = float(product_container.split()[0])
		prices = np.array(prices)*prod_size/cat_size

	# get the most common container in our productid
	#maxlen = 0
	#maxlen_cont = ""
	#for key in catdict[pr].keys():
	#	if len(catdict[pr][key]) > maxlen:
	#		maxlen = len(catdict[pr][key])
	#		maxlen_cont = key
	#product_container = maxlen_cont
	#product_prices = catdict[pr][product_container]

	#prices = {}
	#for prod,val in catdict.iteritems():
	#	if not prod == pr:
	#		for k in val.keys():
	#			if k not in prices:
	#				prices[k] = []
	#			prices[k] = prices[k] + val[k]
	#price_unit_dict = {key:len(value) for key,value in prices.iteritems()}


	#containers = {}
	#for prod,val in catdict.iteritems():
	#	for unit in val.keys():
	#		if not unit in containers:
	#			containers[unit] = 0
	#		containers[unit] += len(val[unit])
	## get the most common container for each category
	#common_unit = max(containers, key=containers.get)

	## get all prices for common container
	#prices = []
	#for prod,val in catdict.iteritems():
	#	if common_unit in val:
	#		prices = prices + val[common_unit]

	## get prices for our product
	#if common_unit in catdict[pr]:
	#	product_prices = catdict[pr][common_unit]
	#else:
	#	# get adjusted prices for most similar container
	#	size = float(common_unit.split()[0])
	#	closest_size_unit = ""
	#	closest_size = 0
	#	size_dist = 10000000
	#	for unit in catdict[pr].keys():
	#		unit_size = float(unit.split()[0])
	#		if np.abs(size-unit_size) < size_dist:
	#			closest_size_unit = unit
	#			closest_size = unit_size
	#			size_dist = np.abs(size-unit_size)
	#	product_prices = np.array(catdict[pr][closest_size_unit])*(size/closest_size)

	# compare price for our products to other products in category with same container

	# store productprice divided by median price in category
	if np.mean(prices) == 0.:
		print "mean is zero"
		import pdb;pdb.set_trace()
	mean_prod = np.mean(product_prices)/np.mean(prices)
	# store productprice divided by mean price in category
	if np.median(prices) == 0.:
		print "median is zero"
		import pdb;pdb.set_trace()
	median_prod = np.median(product_prices)/np.median(prices)
	# store which quantile it is
	median_prod_price = np.median(product_prices)
	sorted_prices = sorted(prices)
	for i, sp in enumerate(sorted_prices):
		if median_prod_price < sp:
			quantile = float(i)/float(len(sorted_prices))
			break
	# median price difference
	median_diff = median_prod_price-np.median(prices)

	product_features[pr] = {'median_rate' : median_prod, 'mean_rate' : mean_prod, 'quantile' : quantile, 'median_difference' : median_diff}

of = open(os.path.join(folder,"product_cheapness_features.csv"), "w")
of.write("product_id,price_quantile,price_median_compare,price_mean_compare,price_median_difference\n")
for pr in productids:
	of.write(pr+","+str(product_features[pr]['quantile'])+","+str(product_features[pr]['median_rate'])+","+str(product_features[pr]['mean_rate'])+","+str(product_features[pr]['median_difference'])+"\n")
