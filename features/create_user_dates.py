# get first and last date of all users

of = open("../data/user_dates.csv","w")
of.write("id,first_date,last_date\n")

fi = open("../data/transactions.csv","r")
fi.next()
li = fi.next().strip().split(",")
lastid = li[0]
startdate = li[6]
prevdate = li[6]
for i,lines in enumerate(fi):
	li = lines.strip().split(",")
	if not lastid == li[0]:
		# write out
		of.write(lastid+","+startdate+","+prevdate+"\n")
		# initalize new
		startdate = li[6]
	prevdate = li[6]
	lastid = li[0]
	if i % 100000 == 0 and i > 0:
		print i
# last entry
of.write(lastid+","+startdate+","+prevdate+"\n")