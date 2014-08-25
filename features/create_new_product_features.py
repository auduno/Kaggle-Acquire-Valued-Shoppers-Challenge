
#- create binary feature on whether user has bought product before (is this indicated by has_bought_prodid? no)
#- create binary feature on whether product is established or not
#- create feature of probability of rebuy in category, based on how frequent they buy in the category (if they do)
#  -take space between buys, take mean and then calculate chance of buy in next quarter? 
#  -estimate probability of rebuy as poisson dist variable, remember that offer date is also a buy-date.
#  -what about no buys in category? 0 prob
#  -mle of lambda in exponential distribution is 1/mean(times between event)
#    -> number of events in time [0,60] follow poisson distribution with parameter 60/mean(times between event)
#    -> probability of P(more than one event) = 1-P(one event) = 1- (60/mean(times between event)*exp(60/mean(times between event)))
#- create feature on if they only bought the product we are interested in, in category
#- create feature on how many different products in the category the user has bought

import string, os, datetime
from collections import defaultdict
import numpy as np

testset = False
if testset:
	folder = "./test/"
	history = "../data/testHistory.csv"
else:
	folder = "./train/"
	history = "../data/trainHistory.csv"

established_products = [
	"3509 103320030 875",
	"7205 103700030 4294",
	"9909 107127979 6732",
	"3203 106414464 13474",
	"5616 104610040 15889",
	"706 104127141 26189",
	"4401 105100050 13791",
	"4517 105450050 1322",
	"5122 107106878 17311"
]

# get ids in history
ids = {}
fi = open(history,"r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	ids[li[0]] = li[1:]

# get offers
offers = {}
fi = open("../data/offers.csv","r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	offers[li[0]] = li[1]+" "+li[3]+" "+li[5]

fi = open("../data/transactions.csv","r")
fi.next()

of = open(os.path.join(folder,"new_product_features.csv"),"w")
of.write("id,bought_product_before,established_product,probability_of_60d_buy_in_category,num_distinct_products_in_cat_bought,only_bought_our_product\n")

last_id = 0
inter_times = []
prods_bought = set([])
prev_date_buy = None

for e,lines in enumerate(fi):
	li = lines.strip().split(",")
	if not last_id == li[0] and e > 0:
		if last_id in ids:
			outline = last_id
			if intprod in prods_bought:
				outline += ",1"
			else:
				outline += ",0"
			if intprod in established_products:
				outline += ",1"
			else:
				outline += ",0"
			if not prev_date_buy is None:
				if testset:
					offer_date = datetime.datetime.strptime(ids[last_id][3], "%Y-%m-%d").date()
				else:
					offer_date = datetime.datetime.strptime(ids[last_id][5], "%Y-%m-%d").date()
				if not offer_date == prev_date_buy:
					inter_times.append( (offer_date-prev_date_buy).days )
				lam = 1./np.mean(inter_times)
				prob = 1.-(np.exp(-60.*lam))
				outline += ","+str(prob)
			else:
				outline += ",0.0"
			outline += ","+str(len(prods_bought))
			if len(prods_bought) == 1 and intprod in prods_bought:
				outline += ",1"
			else:
				outline += ",0"
			outline += "\n"
			of.write(outline)

		# reset variables
		last_id = 0
		prods_bought = set([])
		inter_times = []
		prev_date_buy = None

	if li[0] in ids:
		intprod = offers[ ids[li[0]][1] ]
		intcat = intprod.split(" ")[0]
		if li[3] == intcat:
			prod = string.join(li[3:6]," ")
			prods_bought.add(prod)
			curdate = datetime.datetime.strptime(li[6], "%Y-%m-%d").date()
			if not prev_date_buy is None and not curdate == prev_date_buy:
				inter_times.append( (curdate-prev_date_buy).days )
			prev_date_buy = curdate

	last_id = li[0]
	if e % 1000000 == 0 and e > 0:
		print e

# do the last entry
outline = last_id
if intprod in prods_bought:
	outline += ",1"
else:
	outline += ",0"
if intprod in established_products:
	outline += ",1"
else:
	outline += ",0"
if not prev_date_buy is None:
	if testset:
		offer_date = datetime.datetime.strptime(ids[last_id][3], "%Y-%m-%d").date()
	else:
		offer_date = datetime.datetime.strptime(ids[last_id][5], "%Y-%m-%d").date()
	if not offer_date == prev_date_buy:
		inter_times.append( (offer_date-prev_date_buy).days )
	lam = 1./np.mean(inter_times)
	prob = 1.-(np.exp(-60.*lam))
	outline += ","+str(prob)
else:
	outline += ",0.0"
outline += ","+str(len(prods_bought))
if len(prods_bought) == 1 and intprod in prods_bought:
	outline += ",1"
else:
	outline += ",0"
outline += "\n"
of.write(outline)