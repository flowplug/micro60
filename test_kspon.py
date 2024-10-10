import nov_admin
import pickle
import kspon
import fig
from copy import deepcopy
obb=fig.par()
obb.add_list('conflate',obb.tre['conflate_fullx'])
obb.add_list('conflate_fill',obb.tre['conflate_fillx'])
ob = nov_admin.symb(obb)

fout = 'kspon.txt'
	

def quarter(ray):
	ot = []
	for lo in range(3, len(ray), 4):
		ot += [ray[lo]]
	return ot
       
def main():
	print (ob.pths['curp'])
	ray_dict= {}
	with open('train'+'z'+ob.pths['curp'].replace('/','')+'.pickle', 'rb') as handle:
		ray_dict = pickle.load(handle)
		
	targray = quarter(deepcopy(ray_dict['AAPL']))
	cla = kspon.loc()
	buyr, sellr = cla.main(targray)
	foutt = open(fout, 'w')
	for xx in range(len(targray)):
		foutt.write(str(targray[xx])+','+str(buyr[xx])+','+str(sellr[xx])+'\n')
	foutt.close()


if __name__ == "__main__":
	main()
