# Kaggle Acquire Valued Shoppers Challenge

This is code to generate my submission to the [Kaggle Acquire Valued Shoppers Challenge](http://www.kaggle.com/c/acquire-valued-shoppers-challenge/). This submission managed to give me a 61st place in the competition (under the alias [auduno](http://www.kaggle.com/users/48400/auduno)), enough to be in top 10%. Together with the results on the [Loan Default Prediction challenge](http://www.kaggle.com/c/loan-default-prediction/), this earned me a Kaggle masters badge. Post-deadline, after some hints from forum, fixing the probabilities from different models to be uniform before blending, plus removing some of my models (!), improved my position on leaderboard to 20th place.

The challenge of this competition was to predict which shoppers that responded to a rebate coupon on a specific product, would become repeat buyers of that product. The given dataset was a 22 GB dataset with one year history of transactions for each shopper.

The biggest difficulty in this competition was to create good features from the dataset of transactions. The features I created were roughly:

* features on whether the customer has bought the product/category/brand earlier and also how much they spent and how many units of the product/category/brand they bought (AKA [Triskelions features](http://mlwave.com/predicting-repeat-buyers-vowpal-wabbit/))
* how many visits in last 30 days
* marketshare of each product in the category
* share of customers who bought the product/category
* average price for product
* differences in seasonal spending per product
* general repeat-buy-probabilities for a product based on historical repeat buys
* how much competition a product faces
* how cheap a product is compared to other products
* time since customers first transaction
* whether user had returned the product before

Classification was then based on these features, and was a blend of various models:
* Extra Trees Classifier (scikit-learn)
* Gradient Boosting Classifier with Linear models as base estimators (xgboost)
* Gradient Boosting Classifier with Trees as base estimators (xgboost)
* SVM Classifier fitted with SGD and loop-sampling to optimize area under ROC curve (sofia-ml)
* SVM Classifier fitted with SGD, fitted on power-transformed repeattrips (sofia-ml)
* Quantile Regression (vowpal wabbit) (this was mainly based on triskelions features)

These models were then blended again using Gradient Boosting, trained on a holdout set of the training data.

## To recreate the submission

This submission requires an installation of xgboost, vowpal wabbit, sofia-ml and scikit-learn, and has only been tested on ubuntu linux. Note that since this is a large dataset, creation of features will take a long time, so I've included a zipped file with the finished features in */features/train* and */features/test*. Classification might also take up up to an hour and requires a lot of RAM (> 8 GB), mostly due to the extra trees classifier in scikit-learn.

* download the competion data (*offers.csv*, *testHistory.csv*, *trainHistory.csv*, *transactions.csv*) and put it in the folder "data"
* create some helper data:
 * create_dept_category_map.py
 * create_seasonal_cat.py
 * create_user_dates.py
 * create_base_features.py
* create features by running these scripts. Note that you need to create features for both training and test sets. To switch between running for training and test sets, set the python variable "testset" in the beginning of each script to False or True respectively.
 * create_product_features1.py
 * create_user_features1.py
 * create_seasonal_features.py
 * create_product_cheapness_feature.py
 * create_rebuy_probability_categories.py
 * create_rebuy_probability_products.py
 * create_competition_features.py
 * create_new_product_features.py
 * create_user_first_transaction_feature.py
 * create_negative_features.py
 * merge_features.py
* set positions for installation of xgboost, vw, sofia-ml, data-folder in top of python script *generate_submission.py* via variables *xgboost_python_path*, *vowpalwabbit_path*, *sofiaml_path*, and *data_path*
* run *generate_submission.py* to create the final submission
