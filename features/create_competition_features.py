# competition features

import string, os

testset = False
if testset:
	folder = "./test/"
else:
	folder = "./train/"

categories = [
	"706", "799", "1703", "1726", "2119", "2202", "3203", "3504", "3509", "4401", "4517", "5122", "5558", "5616", "5619", "5824", "6202", "7205", "9115", "9909"
]

productspend_in_cat = {}
for c in categories:
	productspend_in_cat[c] = {}

fi = open("../data/reduced.csv","r")
fi.next()
for lines in fi:
	li = lines.strip().split(",")
	if li[3] in categories:
		productid = string.join(li[3:6]," ")
		if not productid in productspend_in_cat[li[3]]:
			productspend_in_cat[li[3]][productid] = 0.0
		productspend_in_cat[li[3]][productid] += float(li[10])

category_dom_marketshare = {}
category_prod_count = {}

for c in categories:
	catsum = sum(productspend_in_cat[c].values())
	cat_marketshares = []
	for pid in productspend_in_cat[c]:
		cat_marketshares.append(productspend_in_cat[c][pid]/catsum)
	category_dom_marketshare[c] = max(cat_marketshares)
	category_prod_count[c] = len(productspend_in_cat[c])

of = open( os.path.join(folder, "competition_features.csv"),"w")
of.write( "categoryid,competing_products_in_cat,marketshare_dominant_prod_in_cat\n" )
for c in categories:
	of.write(c+","+str(category_prod_count[c])+","+str(category_dom_marketshare[c])+"\n")
