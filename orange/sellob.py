import sys
from joblib import dump, load
import pickle as pic
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
import numpy as np
from numpy import zeros
from collections import OrderedDict
import datetime
from random import randint, uniform

class algi(object):
	def __init__(self, dirr, pybdir, target, hugs):
		self.namm = target
		self.hugs= hugs
		self.dirr = dirr
		self.pybdir = pybdir+'/'
		self.bos = 'sell.csv'
		self.algo ='SAMME.R'
		self.f1 = self.dirr+'aaatrain'+self.bos
		self.f2 = self.dirr+"aaavalid"+self.bos
		self.outf = self.dirr+'/asell'+target+'.csv'
		initfile = False
		self.iters = 2000
		if initfile: 
			open(self.outf,'w')
		self.itrun()			
		
	def readft(self,fin, tak):
		finh = open(fin)
		lins = finh.readlines()
		rows = len(lins)
		mat = zeros((rows,tak))
		targ = zeros((rows))
		cou = -1
		for lin in lins:
			lin = lin.replace('\n','')
			cou+=1
			ist = lin.split(',')
			vaa = float(ist[-1])
			ist = ist[:-1] # The last value is the target and is eliminated, as it was in scikit.py
			targ[cou] = vaa
			ou = -1
			for lo in self.hugs[-1*tak:]:
				ou += 1
				mat [cou][ou] = float(ist[lo])
		return mat, targ

	def sci(self,X_train,y_train,X_test,y_test,nam,depth,trees,learning_ratee,tak):
		regr = AdaBoostClassifier(DecisionTreeClassifier(max_depth=depth),algorithm=self.algo,n_estimators=trees,learning_rate=learning_ratee)
		regr.n_jobs=-1
		regr.fit(X_train, y_train)
		ct = datetime.datetime.now()
		# ts store timestamp of current time
		ts = str(ct.timestamp()).replace('.','_')

		modnamep=nam+'_'+str(trees)+'_'+str(depth)+'_'+self.bos+'_'+str(tak)+'_'+str(learning_ratee)+'_'+self.algo
		modnamep=modnamep.replace('_',',')
		modnamef =nam+'_'+str(trees)+'_'+str(depth)+'_'+self.bos+'_'+str(tak)+'_'+str(learning_ratee)+'_'+ts+'.pyb'
		pic.dump(regr,open(self.pybdir+nam+'_'+str(trees)+'_'+str(depth)+'_'+self.bos+'_'+str(tak)+'_'+str(learning_ratee)+'_'+ts+'.pyb','wb'))
		ans=regr.predict(X_test)
		correct_neg1=0
		correct_one=0
		total_one=0
		total_neg1=0
		total_ans_neg1 = 0
		total_ans_one= 0
		for x in range(len(y_test)):
			if ans[x] ==-1: total_ans_neg1 += 1
			if ans[x] ==1: total_ans_one += 1
			if y_test[x] ==-1: total_neg1+=1
			if y_test[x] ==1: total_one+=1
			if y_test[x] ==-1 and  ans[x]==-1:
				correct_neg1+=1
			if y_test[x] ==1 and  ans[x]==1:
				correct_one+=1
		fru = open (self.outf,'a')
		hugstr = str(self.hugs)
		hugstr = hugstr.replace('[',',')
		hugstr = hugstr.replace(']','')
		fru.write(str(ts)+','+str(correct_neg1)+','+str(correct_one)+','+str(float(correct_neg1)/float(total_neg1))+','
				+str(float(correct_one)/float(total_one))+','+str(float(total_neg1))+','+str(float(total_ans_neg1))+','
				+str(float(total_one))+','+str(float(total_ans_one))+','+modnamep+','+modnamef+','+str(hugstr)+'\n')
		fru.close()
		
	def runran(self):
		tak = randint(1,len(self.hugs))
		depth = randint(4,50)
		trees = randint(50,len(self.hugs))
		lerate = uniform(1,3.5)
		X, y = self.readft(self.f1,tak)
		PX, Py = self.readft(self.f2,tak)
		self.sci(X, y,PX,Py,self.namm,depth,trees,lerate,tak)
		
	def itrun(self):
		for x in range(self.iters):
			print (x)
			self.runran()
		
	


