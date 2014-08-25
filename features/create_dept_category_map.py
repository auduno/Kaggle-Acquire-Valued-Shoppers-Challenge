fi = open("../data/transactions.csv","r")
fi.next()
cat_dept_map = {}
index = 0
for lines in fi:
	index += 1
	li = lines.strip().split(",")
	cat_dept_map[li[3]] = li[2]
	if index % 100000 == 0:
		print index

of = open("../data/cat_dept_map.csv","w")
of.write("category,dept\n")
for k,v in cat_dept_map.iteritems():
	of.write(k+","+v+"\n")
