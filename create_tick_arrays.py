import pickle
import sys
import nov_admin
import fig
obb = fig.par()
# A fully detailed security ticker files at ob.tre
# must be placed at obb.conflate because of code
# in nov_admin.
obb.add_list('conflate', obb.tre['conflate_fullx'])
fout_nasd = open(obb.tre['tick_nasd_file'], 'w')
fout_nyse = open(obb.tre['tick_nyse_file'], 'w')
ob = nov_admin.symb(obb,False,False)

def main():
	ray_dict={}
	path = ob.calc['pickle_dir']+'/'+ob.pths['curp']
	fi = path+'/train'.pickle'
	handle = open(fi, 'rb')
	ray_dict['train'] = pickle.load(handle)
	nasd_list = list(ray_dict['train']['TICK-NASD'][-380:])
	nyse_list = list(ray_dict['train']['TICK-NYSE'][-380:])
	for yy in nasd_list:
		fout_nasd.write(str(yy)+'\n')
	fout_nasd.close()
	for yy in nyse_list:
		fout_nyse.write(str(yy)+'\n')
	fout_nyse.close()
	


main()
print ('Sucessfully wrote files')

