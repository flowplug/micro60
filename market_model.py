import sys
import os
import secdb
import nov_admin
from numpy import zeros
import pickle
import glean
import fig
obb=fig.par()
obb.add_list('conflate',obb.tre['conflate_fullx'])
obb.add_list('conflate_fill',obb.tre['conflate_fillx'])
ob = nov_admin.symb(obb)
print (ob.avg_symbs)
dbob = secdb.dbp()

def fillraydict(ob, ky):
	ray = {}
	intervals= len(ob.rdi[ky]['dtrue'])
	fies = len(ob.fields)
	for sy in ob.avg_symbs:
		ray[sy] = zeros((intervals*fies))
	return ray

def main():
	print (ob.pths['curp'])
	raydict={}
	for ky in ob.rdi.keys():
		if ob.rdi[ky] == {}: continue
		raydict[ky] = fillraydict(ob,ky)
	sqldict ={}
	for ky in ob.rdi.keys():
		if ob.rdi[ky] == {}: continue
		span = [ob.rdi[ky]['dtrue'][0], ob.rdi[ky]['dtrue'][-1]]
		print (span)
		print ('length dtrue', len(ob.rdi[ky]['dtrue']) )
		sqldict[ky] = dbob.getdowm(ob.avg_symbs, span)

	# Put SQL recs into arrays
	for ky in ob.rdi.keys():
		if ob.rdi[ky] == {}: continue
		print (ky)
		glean.glee(sqldict[ky], raydict[ky], ob ,ob.rdi[ky]['dtrue']  )
		# Erase the database dictionary
		#sqldict[ky] ={}
		# Pickle the arrays
		path = ob.pths['pickle_dir']+ob.pths['curp']
		isExist =os.path.exists(path)
		if not isExist:
			os.makedirs(path)
		handle =open(path+'/'+ky+'.pickle', 'wb') 
		pickle.dump(raydict[ky], handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
	main()
