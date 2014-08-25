# get "negative" features:
# bought product just once
# returned product

import datetime,string,os
import numpy as np
from collections import defaultdict

testset = False
if testset:
	folder = "./test/"
else:
	folder = "./train/"

# get products belonging to offer
offers = {}
fi = open("../data/offers.csv","r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	offers[li[0]] = li[1]+" "+li[3]+" "+li[5]

# get history information
history = {}
fi = open("../data/trainHistory.csv","r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	history[li[0]] = li
fi = open("../data/testHistory.csv","r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	history[li[0]] = li
# offer is li[2] here

user_dates = {}
fi = open("../data/user_dates.csv","r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	user_dates[li[0]] = li[2]

of = open( os.path.join(folder, "negative_features.csv"),"w")
of.write("id,returned_product,days_from_lastdata_until_offerdate\n")

fi = open("../data/transactions.csv","r")
fi.next()
# set standard variables
returned = False
lastid = 0

for e,lines in enumerate(fi):
	li = lines.strip().split(",")
	if not lastid == li[0] and e > 0:
		of.write(lastid+",")
		if returned:
			of.write("1,")
		else:
			of.write("0,")

		# get lastdate and offerdate
		offerstuff = history[lastid]
		if len(offerstuff) == 7:
			offerdate = datetime.datetime.strptime(offerstuff[6],"%Y-%m-%d").date()
		else:
			offerdate = datetime.datetime.strptime(offerstuff[4],"%Y-%m-%d").date()
		enddate = datetime.datetime.strptime(user_dates[lastid],"%Y-%m-%d").date()
		daydiff = (offerdate-enddate).days
		of.write(str(daydiff)+"\n")

		# reset values
		returned = False
	user = li[0]
	product = string.join(li[3:6]," ")
	pi = offers[history[li[0]][2]]

	if product == pi:
		if float(li[10]) < 0:
			returned = True
	lastid = li[0]
	if e % 1000000 == 0 and e > 0:
		print e

# last entry
of.write(lastid+",")
if returned:
	of.write("1,")
else:
	of.write("0,")
# get lastdate and offerdate
offerstuff = history[lastid]
if len(offerstuff) == 7:
	offerdate = datetime.datetime.strptime(offerstuff[6],"%Y-%m-%d").date()
else:
	offerdate = datetime.datetime.strptime(offerstuff[4],"%Y-%m-%d").date()
enddate = datetime.datetime.strptime(user_dates[lastid],"%Y-%m-%d").date()
daydiff = (offerdate-enddate).days
of.write(str(daydiff)+"\n")