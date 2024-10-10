
import random
from numpy import linspace
import sys
# ----------------------------------------------------------------
# 1D Brownian motion
# As is standard in Python, use an optional argument to implement what would be
# called a "static auto" in C or a "save parameter" in Fortran -- a local
# variable which is saved between calls.
def B(t, dt, uprev=[0.0]):
	du = random.gauss(0, dt)
	uprev[0] += du
	return uprev[0]

# ----------------------------------------------------------------
def brown(T,dtt,dt, endv,begv):

	ts = list(linspace(0,T, int((T/dtt)-1)))
	ba= list(linspace(begv,endv, int( (T/dtt)-1)))
	nt = len(ts)
	# Brownian motion.
	# Run this first to find out what B(T) turns out to be.
	Bts = []
	ou=-1
	for t in ts:
		ou+=1
		Bt = B(t, dt)
		Bts.append(Bt)
		BT =Bts[-1]
	# Brownian bridge:  R(t) = B(t) - (t/T) B(T).
	Rts = []
	for i in range(0, nt):
		t  = ts[i]
		Bt = Bts[i]
		Rt = Bt - (t/T) * BT 
		Rts.append(Rt)
		
	# Scaled bridge.
	Sb=[begv]
	for z,i in enumerate(ba):
		Sb.append(i+Rts[z])
	return Sb

if __name__=="__main__":
  ki= brown(95*2,1,.05,600,600)
  print (ki)
  print (len(ki))

