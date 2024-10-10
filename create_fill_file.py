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
		print (ky)
		if ky != 'train': continue
		path = ob.pths['pickle_dir']+'/'+ob.pths['curp']
		fi = path+'/'+ky+'.pickle'
		with open(fi, 'rb') as handle:
			ray_dict[ky] = pickle.load(handle)
		fill_list = []
		print (ob.avg_symbs)
		for tik in ob.avg_symbs:
			fill_list += [tik+','+str(ray_dict[ky][tik][-1])]
		print (fill_list)
		fout = open(obb.tre['conflate_fillx'], 'w')
		for strr in fill_list:
			fout.write (strr+'\n')
		fout.close()

main()
print ('Sucessfully wrote: '+obb.tre['conflate_fillx'])

