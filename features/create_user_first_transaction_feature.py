# create features on time since first transaction
import string,datetime, os

testset = False
if testset:
	folder = "./test/"
	history = "../data/testHistory.csv"
else:
	folder = "./train/"
	history = "../data/trainHistory.csv"

user_dates = {}
fi = open("../data/user_dates.csv","r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	startdate = datetime.datetime.strptime(li[1],"%Y-%m-%d").date()
	#enddate = datetime.datetime.strptime(li[2],"%Y-%m-%d").date()
	user_dates[li[0]] = startdate

fi = open(history, "r")
fi.next()
of = open(os.path.join(folder, "first_transaction_features.csv"),"w")
of.write("id,days_since_first_transaction\n")
for lines in fi:
	li = lines.strip().split(",")
	uid = li[0]
	if testset:
		offerdate = datetime.datetime.strptime(li[4],"%Y-%m-%d").date()
	else:
		offerdate = datetime.datetime.strptime(li[6],"%Y-%m-%d").date()
	days_since_first = (offerdate-user_dates[uid]).days
	of.write(uid+","+str(days_since_first)+"\n")
