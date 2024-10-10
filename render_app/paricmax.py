#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
#from mpmath import *
from math import sqrt
import numpy as nu
import os
def paricmax (X ):
	stdX = nu.std(X)
	N= len(X)
	Mx=nu.mean(X)
	x= X-Mx
	if (N*stdX**4) != 0: B2 = nu.sum(x*x*x*x)/(N*(stdX**4))
	else: B2 = 0
	if ((N**2)*(stdX**6)) !=0: B1 = (nu.sum(x*x*x)**2)/((N**2)*(stdX**6))
	else: B1=1
	if B2-B1-1 > 0:
		try:
			icmax = 1/nu.sqrt(B2-B1-1)
		except:  icmax = .5	
	else: icmax = .5
	return icmax
	
	
