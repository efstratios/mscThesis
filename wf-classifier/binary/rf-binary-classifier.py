# -*- coding: utf-8 -*-

import sys, os, argparse
import pandas as pd                     
import numpy as np
from sklearn.preprocessing import LabelEncoder, LabelBinarizer

from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split

from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix

# ################################################### #
#	Our onion website: http://ynvs3km32u33agwq.onion  #
# ################################################### #

def main(): 

	parser = argparse.ArgumentParser(description="Classification and prediction")
	parser.add_argument("--train", required=True, dest="input_train", help="Input csv training dataset")
	parser.set_defaults(feature=False)
	arg = parser.parse_args()

	train = pd.read_csv(arg.input_train, sep=",") # TRAIN DATA

	##### Transforming Nominal Attributes ##### 

	onw_train_le = LabelEncoder()
	onion_website_train_labels = onw_train_le.fit_transform(train['OnionWebsite']) # TRAIN DATASET
	train['OnionWebsite_Label'] = onion_website_train_labels 

	train_sub = train[['OnionWebsite','OnionWebsite_Label','URLPageSize','ObjectPageSize']] 
	
	find_my_onion=train_sub[train_sub['OnionWebsite'].str.startswith('http://ynvs3km32u33agwq', na=False)]
	my_onion = find_my_onion.values[0][0]
	my_onion_label = train_sub.loc[train_sub['OnionWebsite'] == my_onion].iloc[0,1] # find the label of my_onion

	train_df = train_sub.drop('OnionWebsite', axis = 1) 
	
	my_onion_site= (train_df.iloc[0:50000,0] == my_onion_label)
	labelbinarizer = LabelBinarizer()
	onion_website_train_blabels = labelbinarizer.fit_transform(my_onion_site)  
	train_df['OnionWebsite_Label'] = onion_website_train_blabels 
	
	###########################################################################
	############################## RF Classifier ##############################
	###########################################################################
		
	X = train_df.drop('OnionWebsite_Label', axis=1)
	y = train_df['OnionWebsite_Label']


	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=11)

	rfc = RandomForestClassifier()
	rfc.fit(X_train,y_train)
	rfc_predict = rfc.predict(X_test)

	print("=== Confusion Matrix ===")
	print(confusion_matrix(y_test, rfc_predict))
	print('\n')
	print("=== Classification Report ===")
	print(classification_report(y_test, rfc_predict))
	print('\n')

if __name__ == "__main__":
	main()
