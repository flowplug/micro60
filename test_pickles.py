import pickle
import sys
import nov_admin
import fig
obb = fig.par()
# A fully detailed security ticker files at ob.tre
# must be placed at obb.conflate because of code
# in nov_admin.
obb.add_list('conflate', obb.tre['conflate_fullx'])
ob = nov_admin.symb(obb,False,False)

def main():
	ray_dict={}
	for ky in ob.rdi.keys():
		if ob.rdi[ky] == {}: continue
		print (ky)
		path = ob.pths['pickle_dir']+'/'+ob.pths['curp']
		fi = path+'/'+ky+'.pickle'
		with open(fi, 'rb') as handle:
			ray_dict[ky] = pickle.load(handle)
		print (ob.avg_symbs)
		for tik in ob.avg_symbs:
			print (tik, list(ray_dict[ky][tik][:]).count(0.0))

main()


