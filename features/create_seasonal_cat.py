import datetime, string

earliest = datetime.date(2012,3,2)
latest = datetime.date(2013,7,28)

# get all categories we are interested in
categories = [9115, 9909, 3203, 5558, 4401, 1703, 1726, 3504, 3509, 5122, 5616, 5619, 2202, 2119, 6202, 5824, 799, 4517, 7205, 706]

arlen = (latest-earliest).days+1
# create array to contain number of customers on each data
numcust = [0]*arlen
# for each category create same array, and add up for each day seen
catspend = {}
for c in categories:
	catspend[c] = [0.]*arlen

# go through transactions and look at things
fi = open("../data/transactions.csv","r")
fi.next()
last_id = 0
for i,lines in enumerate(fi):
	li = lines.strip().split(",")
	if li[0] != last_id:
		if i > 0:
			# get last_date and write out days to numcust
			initindex = (start_date-earliest).days
			lenindex = (last_date-start_date).days
			for i in range(initindex, initindex+lenindex):
				numcust[i] += 1
		# initialize new users
		start_date = datetime.datetime.strptime(li[6], "%Y-%m-%d").date()
	last_id = li[0]
	last_date = datetime.datetime.strptime(li[6], "%Y-%m-%d").date()
	if int(li[3]) in categories:
		curindex = (last_date-earliest).days
		catspend[int(li[3])][curindex] += float(li[10])
	if i % 100000 == 0 and i > 0:
		print i

# save array somewhere
of = open("../data/seasonal_cat.csv","w")
of.write("date,"+string.join([str(c) for c in categories],",")+",num_customers\n")
for i in range(arlen):
	of.write( (earliest+datetime.timedelta(days=i)).strftime("%Y-%m-%d") )
	for c in categories:
		if numcust[i] > 0:
			of.write("," + str(float(catspend[c][i])/float(numcust[i])) )
		else:
			of.write(",0")
	of.write(","+str(numcust[i])+"\n")
