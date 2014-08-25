# create seasonal feature
import numpy as np
import pandas as pd
import datetime, os

testset = False
if testset:
	folder = "./test/"
	history_file = "../data/testHistory.csv"
else:
	folder = "./train/"
	history_file = "../data/trainHistory.csv"

# load seasonal_cat.csv
seasonal = pd.io.parsers.read_csv("../data/seasonal_cat.csv", index_col=0)
# drop data with low amount of customers
seasonal = seasonal[8:388]

earliest = datetime.date(2012,3,10)
latest = datetime.date(2013,3,24)

categories = ['706', '799', '1703', '1726', '2119', '2202', '3203', '3504', '3509', '4401', '4517', '5122', '5824', '5558', '5616', '5619', '6202', '7205', '9115', '9909']

# calculate trendlines for each category
cat_trend = {}
for c in categories:
  # divide spending in 2013-03-05 - 2013-03-19 by spending in 2012-03-05 - 2012-03-19
  avg2012 = seasonal[c][0:15].mean()
  avg2013 = seasonal[c][365:380].mean()
  cat_trend[c] = avg2013/avg2012

# remove estimated trends from spending (i.e. only get seasonal effects)
for c in categories:
	div = 1. + (cat_trend[c]-1.)*np.array(range(380))/365.
	seasonal[c] = seasonal[c]/div

# sum over similar dates
for c in categories:
	seasonal[c][0:15] = (seasonal[c][0:15]*seasonal['num_customers'][0:15]).values + (seasonal[c][365:380]*seasonal['num_customers'][365:380]).values
	seasonal[c][0:15] /= ( (seasonal['num_customers'][0:15]).values+(seasonal['num_customers'][365:380]).values )
# remove extraneous dates
seasonal = seasonal[0:365]

# get 30 day spending average for each category
cat_spend_avg = {}
for c in categories:
	cat_spend_avg[c] = seasonal[c].mean()*30.

# get offers (for category)
offer_data = {}
fi = open("../data/offers.csv","r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	offer_data[li[0]] = li[1]

fi = open( history_file,"r")
fi.next()
of = open( os.path.join(folder, "seasonal_features.csv"),"w")
of.write("id,seasonal_spend_rate_30d,seasonal_spend_rate_30d_no_trend\n")
for lines in fi:
	li = lines.strip().split(",")
	if testset:
		offerdate = datetime.datetime.strptime(li[4],"%Y-%m-%d").date()
	else:
		offerdate = datetime.datetime.strptime(li[6],"%Y-%m-%d").date()
	offerdateindex = (offerdate-earliest).days
	avg30d = 0.0
	category = offer_data[li[2]]
	# average spending month after offerdate for the category
	for r in range(30):
		avg30d += seasonal[category][(offerdateindex+r) % 365]
	avg30d /= cat_spend_avg[category]
	# then multiply this by the extrapolated trendline from the year ( i.e. (days since 2012-03-12 * trend/365) )
	avg30d_w_trend = avg30d * (offerdateindex+r)/365.*cat_trend[category]
	of.write(li[0]+","+str(avg30d_w_trend)+","+str(avg30d)+"\n")
