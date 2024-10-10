import sys
from joblib import dump, load
import pickle as pic
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
import numpy as np
from numpy import zeros
output_importance_list = 'hugrunMSFTsell.txt'
tris = 50
depth = 2
bos  = 'sell.csv'
algo ='SAMME'
dirr = '../mat_csvs/'
fint = dirr+'aaatrain'+bos
print (bos,algo,depth,tris)
def sci_sort(X_train, y_train,trees):
	regr = AdaBoostClassifier(DecisionTreeClassifier(max_depth=depth),algorithm=algo,n_estimators=tris)
	regr.n_estimators =X_train.shape[1]+tris
	regr.n_jobs=-1
	regr.compute_importances = True
	regr.fit(X_train, y_train)
	fout = open(output_importance_list,'w')
	fout.write (str(list(np.argsort(regr.feature_importances_)))+'\n')
	fout.close()
	
def readf(fin):
	finh = open(fin)
	lins = finh.readlines()
	rows = len(lins)
	samp = lins[0].replace('\n','')
	slist = samp.split(',')
	cols = len(slist) -1 # last column is excluded because it is the target.
	mat = zeros((rows,cols))
	targ = zeros((rows))
	cou = -1
	for lin in lins:
		lin = lin.replace('\n','')
		cou+=1
		ist = lin.split(',')
		vaa = float(ist[-1]) # last column is the target.
		targ[cou] = vaa
		trung =ist[:-1]
		ou = -1
		for it in trung:
			ou += 1
			mat [cou][ou] = float(it)
	return mat, targ

X, y = readf(fint)
sci_sort(X, y,tris)
