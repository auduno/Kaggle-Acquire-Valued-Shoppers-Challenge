
xgboost_python_path = "/home/audun/xgboost-master/python/"
vowpalwabbit_path = "~/vowpal_wabbit/vowpalwabbit/vw"
sofiaml_path = "~/sofia-ml-read-only/sofia-ml"
data_path = "/home/audun/github/Kaggle_Acquire_Valued_Shoppers_Challenge/data/" # this needs to be the full path to the data folder

import sys, pickle, string, os
sys.path.append(xgboost_python_path)
import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from subprocess import call
from sklearn.datasets import dump_svmlight_file
from sklearn.cross_validation import ShuffleSplit

offer_est_weights = [1200988, 1194044, 1197502, 1204576, 1199256, 1199258]

predictions = {}

for r in range(3):
	# get data
	test_data = pd.io.parsers.read_csv("./features/test/all_features.csv", sep=" ")
	train_data = pd.io.parsers.read_csv("./features/train/all_features.csv", sep=" ")

	split = ShuffleSplit(train_data.shape[0], n_iter = 1, test_size=0.10)
	for tr, te in split:
		train1, train2 = tr, te

	train1_data = train_data.iloc[train1,:]
	train2_data = train_data.iloc[train2,:]

	train1_label = train1_data['label']
	train1_label_rep = train1_data['repeattrips']
	train2_label = train2_data['label']
	train2_label_rep = train2_data['repeattrips']
	del train1_data['label']
	del train2_data['label']
	del train1_data['repeattrips']
	del train2_data['repeattrips']
	del test_data['label']
	del test_data['repeattrips']

	test_ids = test_data['id'].values

	sample_weights = np.ones((train1_data.shape[0],1))
	for ofew in offer_est_weights:
		sample_weights[(train1_data['offer_id'] == ofew).values,0] = 5.

	test_offer_ids = test_data['offer_id']

	# remove features which degrade results
	del train1_data['offer_id']
	del train2_data['offer_id']
	del test_data['offer_id']
	#del train1_data['market']
	#del train2_data['market']
	#del test_data['market']
	del train1_data['marketshare_dominant_prod_in_cat']
	del train2_data['marketshare_dominant_prod_in_cat']
	del test_data['marketshare_dominant_prod_in_cat']
	del train1_data['repeat_buy_prob_90d']
	del train2_data['repeat_buy_prob_90d']
	del test_data['repeat_buy_prob_90d']
	#del train_data['repeat_buy_prob_60d']
	#del test_data['repeat_buy_prob_60d']
	del train1_data['repeat_buy_prob_30d']
	del train2_data['repeat_buy_prob_30d']
	del test_data['repeat_buy_prob_30d']
	del train1_data['prodid_spend_corr']
	del train2_data['prodid_spend_corr']
	del test_data['prodid_spend_corr']
	del train1_data['avg_price_per_cheapest_common_unit']
	del train2_data['avg_price_per_cheapest_common_unit']
	del test_data['avg_price_per_cheapest_common_unit']
	del train1_data['price_mean_compare']
	del train2_data['price_mean_compare']
	del test_data['price_mean_compare']
	del train1_data['has_bought_brand_a_60']
	del train2_data['has_bought_brand_a_60']
	del test_data['has_bought_brand_a_60']
	del train1_data['prodid_spend_all']
	del train2_data['prodid_spend_all']
	del test_data['prodid_spend_all']
	del train1_data['chain']
	del train2_data['chain']
	del test_data['chain']
	del train1_data['id']
	del train2_data['id']
	del test_data['id']
	del train1_data['seasonal_spend_rate_30d']
	del train2_data['seasonal_spend_rate_30d']
	del test_data['seasonal_spend_rate_30d']
	del train1_data['share_of_cust_bought_prod']
	del train2_data['share_of_cust_bought_prod']
	del test_data['share_of_cust_bought_prod']
	del train1_data['price_quantile']
	del train2_data['price_quantile']
	del test_data['price_quantile']
	del train1_data['price_median_compare']
	del train2_data['price_median_compare']
	del test_data['price_median_compare']
	del train1_data['avg_price_per_most_common_unit']
	del train2_data['avg_price_per_most_common_unit']
	del test_data['avg_price_per_most_common_unit']

	del train1_data['established_product']
	del train2_data['established_product']
	del test_data['established_product']
	del train1_data['probability_of_60d_buy_in_category']
	del train2_data['probability_of_60d_buy_in_category']
	del test_data['probability_of_60d_buy_in_category']
	del train1_data['num_distinct_products_in_cat_bought']
	del train2_data['num_distinct_products_in_cat_bought']
	del test_data['num_distinct_products_in_cat_bought']
	del train1_data['only_bought_our_product']
	del train2_data['only_bought_our_product']
	del test_data['only_bought_our_product']

	del train1_data["never_bought_category"]
	del train2_data["never_bought_category"]
	del test_data["never_bought_category"]
	del train1_data["never_bought_brand"]
	del train2_data["never_bought_brand"]
	del test_data["never_bought_brand"]
	del train1_data["never_bought_company"]
	del train2_data["never_bought_company"]
	del test_data["never_bought_company"]


	del train1_data['marketshare_in_dep']
	del train2_data['marketshare_in_dep']
	del test_data['marketshare_in_dep']
	#del train_data['share_of_cust_bought_dep']
	#del test_data['share_of_cust_bought_dep']
	del train1_data['share_dep_spend']
	del train2_data['share_dep_spend']
	del test_data['share_dep_spend']

	print "training extra trees forest"
	clf = ExtraTreesClassifier(n_estimators=1000, n_jobs=8)
	clf.fit(train1_data, train1_label, sample_weight=sample_weights[:,0])
	pred_label3 = clf.predict_proba(train2_data)[:,1]
	pred_label_test3 = clf.predict_proba(test_data)[:,1]

	# train on training set 
	dtrain1 = xgb.DMatrix( train1_data.values, label=train1_label.values, weight=sample_weights)
	dtrain2 = xgb.DMatrix( train2_data.values, label=train2_label.values)
	dtest = xgb.DMatrix( test_data.values)

	# train 
	print "training gbc:tree boosters"
	param = {'bst:max_depth':3, 'bst:eta':0.1, 'silent':1, 'objective':'binary:logistic', 'nthread' : 8, 'eval_metric':'auc' }
	num_round = 100
	bst = xgb.train( param, dtrain1, num_round)

	pred_label1 = bst.predict( dtrain2 )
	pred_label_test1 = bst.predict( dtest )

	pred_train = np.hstack(( np.reshape(pred_label1,(-1,1)), np.reshape(pred_label3,(-1,1)) ))
	pred_test = np.hstack(( np.reshape(pred_label_test1,(-1,1)), np.reshape(pred_label_test3,(-1,1)) ))

	# predict sofia-ml

	print "training sgd-svm"
	names = train1_data.columns
	## normalize data?
	ss = StandardScaler()
	train1_data_norm = ss.fit_transform(train1_data)
	train2_data_norm = ss.transform(train2_data)
	test_data_norm = ss.transform(test_data)

	model_file = os.path.join(data_path,"sofml.model")
	training_file = os.path.join(data_path, "train_data.dat")
	training2_file = os.path.join(data_path,"train2_data.dat")
	test_file = os.path.join(data_path, "test_data.dat")
	pred_train2_file = os.path.join(data_path, "pred_train2.csv")
	pred_test_file = os.path.join(data_path, "pred_test.csv")

	# write out traindata and testdata to svmlight format
	print "writing out files"	
	ntrain1_label = train1_label.copy()
	ntrain1_label.values[np.where(ntrain1_label == 0)] = -1
	ntrain2_label = train2_label.copy()
	ntrain2_label.values[np.where(ntrain2_label == 0)] = -1
	dump_svmlight_file(train1_data_norm, ntrain1_label, training_file, zero_based=False)
	dump_svmlight_file(train2_data_norm, ntrain2_label, training2_file, zero_based=False)
	dump_svmlight_file(test_data_norm, np.zeros((test_data_norm.shape[0],)), test_file, zero_based=False)

	# train
	#print "training sofia"
	call(sofiaml_path+" --learner_type sgd-svm --loop_type roc --prediction_type logistic --iterations 200000 --lambda 10000 --training_file "+training_file+" --model_out "+model_file, shell=True)

	# predict
	#print "predicting sofia"
	call(sofiaml_path+" --model_in "+model_file+" --test_file "+training2_file+" --results_file "+pred_train2_file, shell=True)
	call(sofiaml_path+" --model_in "+model_file+" --test_file "+test_file+" --results_file "+pred_test_file, shell=True)

	# read in predictions

	pred_label4 = pd.io.parsers.read_csv(pred_train2_file, sep="\t", names=["pred","true"])['pred']
	pred_label_test4 = pd.io.parsers.read_csv(pred_test_file, sep="\t", names=["pred","true"])['pred']

	pred_train = np.hstack(( pred_train, np.reshape(pred_label4,(-1,1)) ))
	pred_test = np.hstack(( pred_test, np.reshape(pred_label_test4,(-1,1)) ))

	#######

	#print "training sofia-ml logreg-pegasos"
	#call("~/sofia-ml-read-only/sofia-ml --learner_type logreg-pegasos --loop_type roc --iterations 200000 --prediction_type logistic --lambda 10000 --training_file "+training_file+" --model_out "+model_file, shell=True)
	#call("~/sofia-ml-read-only/sofia-ml --model_in "+model_file+" --test_file "+training2_file+" --results_file "+pred_train2_file, shell=True)
	#call("~/sofia-ml-read-only/sofia-ml --model_in "+model_file+" --test_file "+test_file+" --results_file "+pred_test_file, shell=True)
	#pred_label5 = pd.io.parsers.read_csv(pred_train2_file, sep="\t", names=["pred","true"])['pred']
	#pred_label_test5 = pd.io.parsers.read_csv(pred_test_file, sep="\t", names=["pred","true"])['pred']
	#pred_train = np.hstack(( pred_train, np.reshape(pred_label5,(-1,1)) ))
	#pred_test = np.hstack(( pred_test, np.reshape(pred_label_test5,(-1,1)) ))

	#######

	# new linear regression on transformed variables

	#dtrain1 = xgb.DMatrix( train1_data.values, label=np.power(train1_label_rep.values, 2./3.), weight=sample_weights)
	#dtrain2 = xgb.DMatrix( train2_data.values, label=np.power(train2_label_rep.values, 2./3.))

	#print "training gbc linear regression on transformed variables"
	#param = {'booster_type':1, 'bst:lambda':0, 'bst:alpha':0, 'bst:lambda_bias':0, 'silent':1, 'objective':'reg:linear', 'nthread' : 4, 'eval_metric':'auc' }
	#num_round = 20
	#bst = xgb.train( param, dtrain1, num_round)

	#pred_label5 = bst.predict( dtrain2 )
	#pred_label5 = np.power(np.clip(pred_label5,0,np.inf), 3./2.)
	#pred_label_test5 = bst.predict( dtest )
	#pred_label_test5 = np.power(np.clip(pred_label_test5,0,np.inf), 3./2.)

	#pred_train = np.hstack(( pred_train, np.reshape(pred_label5,(-1,1)) ))
	#pred_test = np.hstack(( pred_test, np.reshape(pred_label_test5,(-1,1)) ))

	#######

	# sofia ml on transformed variables 

	print "training sofia SVM sgd on power-transformed repeattrips"

	model_file = os.path.join(data_path, "sofml.model")
	training_file = os.path.join(data_path, "train_data.dat")
	training2_file = os.path.join(data_path, "train2_data.dat")
	test_file = os.path.join(data_path, "test_data.dat")
	pred_train2_file = os.path.join(data_path, "pred_train2.csv")
	pred_test_file = os.path.join(data_path, "pred_test.csv")

	# write out traindata and testdata to svmlight format
	print "writing out files for sofia-ml"	
	ntrain1_label = np.power(train1_label_rep.values, 2./3. )
	ntrain2_label = np.power(train2_label_rep.values, 2./3. )
	dump_svmlight_file(train1_data_norm, ntrain1_label, training_file, zero_based=False)
	dump_svmlight_file(train2_data_norm, ntrain2_label, training2_file, zero_based=False)
	dump_svmlight_file(test_data_norm, np.zeros((test_data_norm.shape[0],)), test_file, zero_based=False)

	# train
	call(sofiaml_path+" --learner_type sgd-svm --loop_type roc --prediction_type linear --iterations 200000 --lambda 10 --training_file "+training_file+" --model_out "+model_file, shell=True)

	# predict
	call(sofiaml_path+" --model_in "+model_file+" --test_file "+training2_file+" --results_file "+pred_train2_file, shell=True)
	call(sofiaml_path+" --model_in "+model_file+" --test_file "+test_file+" --results_file "+pred_test_file, shell=True)

	# read in predictions		
	pred_label6 = pd.io.parsers.read_csv(pred_train2_file, sep="\t", names=["pred","true"])['pred']
	pred_label6 = np.power(np.clip(pred_label6,0,np.inf), 3./2.)
	pred_label_test6 = pd.io.parsers.read_csv(pred_test_file, sep="\t", names=["pred","true"])['pred']
	pred_label_test6 = np.power(np.clip(pred_label_test6,0,np.inf), 3./2.)

	pred_train = np.hstack(( pred_train, np.reshape(pred_label6,(-1,1)) ))
	pred_test = np.hstack(( pred_test, np.reshape(pred_label_test6,(-1,1)) ))

	############### add quantile regression:

	ntrain1_label = train1_label.copy()
	ntrain1_label.values[np.where(ntrain1_label == 0)] = -1
	ntrain2_label = train2_label.copy()
	ntrain2_label.values[np.where(ntrain2_label == 0)] = -1
	dump_svmlight_file(train1_data, ntrain1_label, training_file, zero_based=False)
	dump_svmlight_file(train2_data, ntrain2_label, training2_file, zero_based=False)
	dump_svmlight_file(test_data, np.zeros((test_data_norm.shape[0],)), test_file, zero_based=False)
	# convert to vowpal wabbit format
	of = open( os.path.join(data_path, "vw_train1set.csv") ,"w")
	of2 = open( os.path.join(data_path, "vw_train2set.csv") ,"w")
	of3 = open( os.path.join(data_path, "vw_testset.csv") ,"w")
	fi = open(training_file)
	for lines in fi:
		li = lines.strip().split()
		of.write( li[0] )
		of.write(" | ")
		of.write( string.join(li[1:]," "))
		of.write("\n")
	of.close()
	fi = open(training2_file)
	for lines in fi:
		li = lines.strip().split()
		of2.write( li[0] )
		of2.write(" | ")
		of2.write( string.join(li[1:]," "))
		of2.write("\n")
	of2.close()
	fi = open(test_file)
	for lines in fi:
		li = lines.strip().split()
		of3.write( li[0] )
		of3.write(" | ")
		of3.write( string.join(li[1:]," "))
		of3.write("\n")
	of3.close()

	training_file = os.path.join(data_path, "vw_train1set.csv")
	training2_file = os.path.join(data_path, "vw_train2set.csv")
	model_file = os.path.join(data_path, "vw_trainset_model.vw")
	test_file = os.path.join(data_path, "vw_testset.csv")
	pred_train2_file = os.path.join(data_path, "vwpreds_train2.txt")
	pred_test_file = os.path.join(data_path, "vwpreds_test.txt")

	call(vowpalwabbit_path+" "+training_file+" -c -k --passes 40 -l 0.85 -f "+model_file+" --loss_function quantile", shell=True)
	call(vowpalwabbit_path+" "+training2_file+" -t -i "+model_file+" -r "+pred_train2_file, shell=True)
	call(vowpalwabbit_path+" "+test_file+" -t -i "+model_file+" -r "+pred_test_file, shell=True)

	# load predictions
	pred_label7 = []
	fi = open( os.path.join(data_path, "vwpreds_train2.txt") ,"r")
	for lines in fi:
		li = lines.strip().split()
		pred_label7.append( 1./(1.+np.exp(-float(li[0]))) )
	pred_label_test7 = []
	fi = open( os.path.join(data_path, "vwpreds_test.txt") ,"r")
	for lines in fi:
		li = lines.strip().split()
		pred_label_test7.append( 1./(1.+np.exp(-float(li[0]))) )

	pred_train = np.hstack(( pred_train, np.reshape(pred_label7,(-1,1)) ))
	pred_test = np.hstack(( pred_test, np.reshape(pred_label_test7,(-1,1)) ))


	########

	del train1_data['has_bought_company_30']
	del train2_data['has_bought_company_30']
	del test_data['has_bought_company_30']
	del train1_data['has_bought_company_q_60']
	del train2_data['has_bought_company_q_60']
	del test_data['has_bought_company_q_60']
	del train1_data['has_bought_category_60']
	del train2_data['has_bought_category_60']
	del test_data['has_bought_category_60']
	del train1_data['has_bought_company_q_30']
	del train2_data['has_bought_company_q_30']
	del test_data['has_bought_company_q_30']
	del train1_data['has_bought_category_q_60']
	del train2_data['has_bought_category_q_60']
	del test_data['has_bought_category_q_60']
	del train1_data['has_bought_company_q_90']
	del train2_data['has_bought_company_q_90']
	del test_data['has_bought_company_q_90']
	del train1_data['has_bought_category_q_30']
	del train2_data['has_bought_category_q_30']
	del test_data['has_bought_category_q_30']
	del train1_data['has_bought_brand_90']
	del train2_data['has_bought_brand_90']
	del test_data['has_bought_brand_90']
	del train1_data['has_bought_brand_180']
	del train2_data['has_bought_brand_180']
	del test_data['has_bought_brand_180']
	del train1_data['has_bought_brand_60']
	del train2_data['has_bought_brand_60']
	del test_data['has_bought_brand_60']
	del train1_data['has_bought_category_a_60']
	del train2_data['has_bought_category_a_60']
	del test_data['has_bought_category_a_60']
	del train1_data['has_bought_company_q_180']
	del train2_data['has_bought_company_q_180']
	del test_data['has_bought_company_q_180']
	del train1_data['has_bought_category_q_90']
	del train2_data['has_bought_category_q_90']
	del test_data['has_bought_category_q_90']
	del train1_data['has_bought_category_90']
	del train2_data['has_bought_category_90']
	del test_data['has_bought_category_90']
	del train1_data['has_bought_brand_q_90']
	del train2_data['has_bought_brand_q_90']
	del test_data['has_bought_brand_q_90']
	del train1_data['has_bought_company_a']
	del train2_data['has_bought_company_a']
	del test_data['has_bought_company_a']
	del train1_data['has_bought_company_a_30']
	del train2_data['has_bought_company_a_30']
	del test_data['has_bought_company_a_30']
	del train1_data['has_bought_category_a_90']
	del train2_data['has_bought_category_a_90']
	del test_data['has_bought_category_a_90']
	del train1_data['has_bought_category_180']
	del train2_data['has_bought_category_180']
	del test_data['has_bought_category_180']
	del train1_data['has_bought_brand_a_30']
	del train2_data['has_bought_brand_a_30']
	del test_data['has_bought_brand_a_30']
	del train1_data['has_bought_brand_a']
	del train2_data['has_bought_brand_a']
	del test_data['has_bought_brand_a']
	del train1_data['has_bought_company_q']
	del train2_data['has_bought_company_q']
	del test_data['has_bought_company_q']
	del train1_data['has_bought_category_q_180']
	del train2_data['has_bought_category_q_180']
	del test_data['has_bought_category_q_180']
	del train1_data['prodid_spend_30']
	del train2_data['prodid_spend_30']
	del test_data['prodid_spend_30']

	dtrain1 = xgb.DMatrix( train1_data.values, label=train1_label.values, weight=sample_weights)
	dtrain2 = xgb.DMatrix( train2_data.values, label=train2_label.values)
	dtest = xgb.DMatrix( test_data.values)

	print "training gbc:linear boosters"
	param = {'booster_type':1, 'bst:lambda':0, 'bst:alpha':0, 'bst:lambda_bias':0, 'silent':1, 'objective':'binary:logistic', 'nthread' : 8, 'eval_metric':'auc' }
	num_round = 35
	bst = xgb.train( param, dtrain1, num_round)

	pred_label2 = bst.predict( dtrain2 )
	pred_label_test2 = bst.predict( dtest )

	pred_train = np.hstack(( pred_train, np.reshape(pred_label2,(-1,1)) ))
	pred_test = np.hstack(( pred_test, np.reshape(pred_label_test2,(-1,1)) ))

	############### BLEND


	dtrain2 = xgb.DMatrix( pred_train, label=train2_label.values)
	dtest = xgb.DMatrix( pred_test )

	print "training blend : xgb trees booster logistic regression, max depth 2"
	param = {'bst:max_depth':2, 'bst:eta':0.1, 'silent':1, 'objective':'binary:logistic', 'nthread' : 8, 'eval_metric':'auc' }
	num_round = 50
	bst = xgb.train( param, dtrain2, num_round)

	pred_label_test = bst.predict( dtest )

	print "training blend : xgb linear booster logistic regression"
	param = {'booster_type':1, 'bst:lambda':0, 'bst:alpha':0, 'bst:lambda_bias':0, 'silent':1, 'objective':'binary:logistic', 'nthread' : 8, 'eval_metric':'auc' }
	num_round = 25
	bst = xgb.train( param, dtrain2, num_round)

	pred_label = bst.predict( dtest )		

	mean_pred = (pred_label + pred_label_test)/2.

	predictions[r] = mean_pred

bagged_prediction = (predictions[0]+predictions[1]+predictions[2])/3.

from time import gmtime, strftime

# write out to file
of = open("./submission_"+ strftime("%d-%m_%H.%M.%S",gmtime()) +".csv","w")
of.write("id,repeatProbability\n")
for i in range(len(test_ids)):
	of.write( "%d,%.12f\n" % (test_ids[i], bagged_prediction[i]) )
