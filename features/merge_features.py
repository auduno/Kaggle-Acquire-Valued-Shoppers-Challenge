import string, os
# merge features

testset = False

if testset:
	folder = "./test/"
else:
	folder = "./train/"

offers_dict = {}
fi = open( "../data/offers.csv" ,"r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	offers_dict[li[0]] = li[1]+" "+li[3]+" "+li[5]

userfeature_dict = {}
fi = open( os.path.join(folder,"user_features.csv"), "r" )
userheaders = fi.next().strip().split(",")
for lines in fi:
	li = lines.strip().split(",")
	userfeature_dict[li[0]] = li[1:]

prodfeature_dict = {}
fi = open( os.path.join(folder, "product_features.csv") ,"r")
prodheaders = fi.next().strip().split(",")
for lines in fi:
	li = lines.strip().split(",")
	prodfeature_dict[li[0]] = li[1:]

# get seasonal features
seasonal_dict = {}
fi = open( os.path.join(folder, "seasonal_features.csv") ,"r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	seasonal_dict[li[0]] = [li[1],li[2]]

# get cheapness features
cheapness_dict = {}
fi = open( os.path.join(folder, "product_cheapness_features.csv"),"r")
cheapness_header = fi.next().strip().split(",")[1:]
for lines in fi:
	li = lines.strip().split(",")
	cheapness_dict[li[0]] = [li[1],li[2],li[3],li[4]]

# get rebuy-probability
rebuy_probability_dict = {}
fi = open(os.path.join(folder, "product_repeat_buy_probability.csv"),"r")
rebuy_probability_header = fi.next().strip().split(",")[1:]
for lines in fi:
	li = lines.strip().split(",")
	rebuy_probability_dict[ li[0] ] = li[1:]

# get competition-features
competition_dict = {}
fi = open(os.path.join(folder, "competition_features.csv"),"r")
competition_header = fi.next().strip().split(",")[1:]
for lines in fi:
	li = lines.strip().split(",")
	competition_dict[ li[0] ] = li[1:]

# get new product features
new_prodfeature_dict = {}
fi = open( os.path.join(folder, "new_product_features.csv") ,"r")
new_prodheaders = fi.next().strip().split(",")
for lines in fi:
	li = lines.strip().split(",")
	new_prodfeature_dict[li[0]] = li[1:]

# get new daydiff features
#daydiff_dict = {}
#fi = open( "../data/daydiff.csv" ,"r")
#for lines in fi:
#	li = lines.strip().split(",")
#	daydiff_dict[li[0]] = li[2]

# get first_transaction features
first_trans_dict = {}
fi = open(os.path.join(folder, "first_transaction_features.csv"),"r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	first_trans_dict[li[0]] = li[1]

# get negative features
negative_dict = {}
fi = open(os.path.join(folder, "negative_features.csv"),"r")
negative_headers = fi.next().strip().split(",")[1:]
for lines in fi:
	li = lines.strip().split(",")
	negative_dict[li[0]] = li[1:]

fi = open( os.path.join(folder, "base_features.csv") ,"r")
headers_orig = fi.next().strip().split()
of = open( os.path.join(folder, "all_features.csv") ,"w")
of.write(
	string.join(headers_orig," ")+" "+string.join(userheaders[1:]," ")+" "+string.join(prodheaders[1:]," ")+\
	" seasonal_spend_rate_30d seasonal_spend_rate_30d_notrend "+\
	string.join(cheapness_header, " ")+" "+string.join(rebuy_probability_header, " ")+" "+ string.join(competition_header," ")+" "+\
	string.join(new_prodheaders[1:], " ")+" days_since_first_transaction "+string.join(negative_headers," ")+"\n"
)

for i,lines in enumerate(fi):
	of.write(lines.strip()+" ")
	li = lines.strip().split()
	of.write( string.join(userfeature_dict[li[2]]," ")+" ")
	prodid = offers_dict[li[3]]
	of.write( string.join(prodfeature_dict[prodid]," ")+" ")
	of.write( string.join(seasonal_dict[li[2]]," ") + " ")
	of.write( string.join(cheapness_dict[prodid]," ")+" " )
	of.write( string.join(rebuy_probability_dict[prodid]," ")+" " )
	of.write( string.join(competition_dict[ prodid.split()[0] ]," ") + " " )
	of.write( string.join(new_prodfeature_dict[ li[2] ]," ") + " " )
	of.write( first_trans_dict[li[2]] + " ")
	of.write( string.join(negative_dict[li[2]], " ") + "\n")
	#if li[2] in negative_dict:
	#	of.write( string.join(negative_dict[li[2]], " ") + "\n")
	#else:
	#	of.write("0 0\n")
	#of.write( daydiff_dict[li[2]] + "\n" )
	if i % 100000 == 0:
		print i
