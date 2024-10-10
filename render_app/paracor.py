#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
#from mpmath import *
from math import sqrt
import numpy as nu
import os
def paracor (X,Y ):
	if len(X) != len (Y):
		print ('The X and Y arrays are not of the same length.')
		sys.exit()
	# Put array elements in multiple precision format.
	sX=nu.sum(X)
	sY=nu.sum(Y)
	sXX=nu.sum(X*X)
	sYY=nu.sum(Y*Y)
	sXY=nu.sum(X*Y)
	sXsqY= nu.sum(X*X)*nu.sum(Y)
	sXcu=nu.sum(X*X*X)
	sXfo=nu.sum(X*X*X*X)
	stdX = nu.std(X)
	stdY= nu.std(Y)
	N= len(X)
	Mx=nu.mean(X)
	x= X-Mx
	if (N*stdX**4) != 0: B2 = nu.sum(x*x*x*x)/(N*(stdX**4))
	else: B2 = 0
	if ((N**2)*(stdX**6)) !=0: B1 = (nu.sum(x*x*x)**2)/((N**2)*(stdX**6))
	else: B1=1
	ctop=(sXsqY-N*sXsqY)*(N*sXX-sX**2)+(N*sXY-sX*sY)*(N*sXcu-sXX*sX)
	cbot=((N*sXcu-sXX*sX)**2)+(((sXX**2)**2)-N*sXfo)*(N*sXX-sX**2)
	if cbot != 0:
		c = ctop / cbot
	else:
		return 0,0,0,0,0,0 #isx,ixcc,ic,cri, icmax, inflectc = 0
	if (N * sXX - sX ** 2) == 0:
		return 0,0,0,0,0,0
	else:
		b = ((N * sXY - sX * sY) - (c * (N * sXcu - sXX * sX))) / (N * sXX - sX ** 2)
		a = (sY - c * sXX - b * sX) / N
	if 2*c != 0:
		inflect= (b/(2*c))/800
	else:
		inflect = 0
	if cbot == 0: c=0
	else:c = ctop/cbot
	if list(X).count(X[0])==len(X) and list(Y).count(Y[0])==len(Y): to =0
	else:	to=nu.corrcoef(X,Y)[0,1]#pearsoncorr2(list(X),list(Y))#nu.corrcoef(X,Y)[0,1]
	if ((N**2)*stdX*stdY)==0:t1=0
	else:t1=(c*(N*sXcu-N* nu.mean(X)*sXX))/((N**2)*stdX*stdY)
	if stdY == 0: ic=0
	else:
		# The index of curvature is computed with
		# equation (10a) on page 63. It is a single statistic
		# for the whole parabola. This is a useful atatistic with
		# a window moving on a time series.
		ratio_top = N*sXX - nu.power(sX,2)
		try:
			ratio_bot = N * sqrt(N*sYY-nu.power(sY,2))
		except:
			return 0, 0, 0, 0, 0, 0
		ic= c * (ratio_top/ratio_bot)
		#print (ic)
	curx = X[len(X)-1]
	if ((N**2)*stdX*stdY)==0:t2=0
	else:t2= (2*c*curx*(N**2)*(stdX**2))/((N**2)*stdX*stdY)
	isx=to-t1+t2
	if (2*N*stdX**2) == 0: critX=0
	else:critX=(sXcu-nu.mean(X)*sXX)/(2*N*stdX**2)
	#xxx= mpf(nu.sum(x*x*x))
	#cRad =mpf( nu.sqrt((xxx**2)/((N**2)*(stdX**6))))
	#critb = nu.mean(X)+.5*stdX*cRad # This is an alternative method to compute crit.
	if str(isx)=='nan' or str(isx) == 'inf' : isx =0
	if str(curx)=='nan' or str(curx) == 'inf' : curx =0
	if str(ic)=='nan' or str(ic) == 'inf' : ic =0
	if B2-B1-1 > 0:
		icmax = 1/nu.sqrt(B2-B1-1)
		#print ('ic ',ic)
		#print ('icmax ',icmax)
	else: icmax=ic
	if str(icmax)=='nan' or str(icmax) == 'inf' or str(icmax)[0]=='(' : icmax =ic
	#if ic >2: ic =2
	#if ic <-2: ic = -2
	#if icmax >2: icmax =2
	#if icmax <-2: icmax = -2
	ixcc=isx*curx
	#if ixcc <-12:ixcc =-12
	#if ixcc >12: ixcc=12
	if Mx:cri=(Mx-critX)/Mx
	else: cri=0
	if cri<-5:cri=-5
	if cri>5:cri=5
	if isx >5: isx=5
	if isx < -5: isx=-5
	return isx,ixcc,cri,ic, icmax, inflect
