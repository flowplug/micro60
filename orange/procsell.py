import os
from collections import OrderedDict
import fig
import aanonan
import scikit
from multiprocessing import Process
import sellob

def importance_order(dirg,dirk,bos,targ,hugs):
	fin = open (dirg)
	lis = fin.readlines()
	coldict = OrderedDict()
	for li in lis:
		lsplit = li.split(',')
		coldict[int(lsplit[0])] = ','.join(lsplit[1:])
	fout = open (dirk+'mapargs'+bos+targ+'.txt', 'w')
	for x in hugs:
		fout.write(str(x)+': '+coldict[x])
	fout.close()
	
ob = fig.par()
path_col_names = ob.pths['label_dir']+ob.pths['curp']+'/'+ ob.calc['column_names_file']
pth = ob.pths['label_dir']+ob.pths['curp']+ob.calc['train_targ']+'/'
pathpyb = pth + ob.pths['pybdir']
isExist = os.path.exists(pathpyb)
if not isExist:
	os.makedirs(pathpyb)
hugs = scikit.main(pth+ob.calc['fins_prefix']+'trainsell.csv',pth+'/mapsell.txt')
importance_order(path_col_names,pth,'sell',ob.calc['train_targ'],hugs)
pcs = [Process(target=sellob.algi, args=(pth,pathpyb,ob.calc['train_targ'],hugs)) for _ in range(int(ob.calc['procsell']))]
for p in pcs:
    p.start()

		

