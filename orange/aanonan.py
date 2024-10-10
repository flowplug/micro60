import sys

nans_replaced={}
infs_replaced={}
large_int = 999999
line_limit_valid_buy = large_int
line_limit_valid_sell = large_int
def figx(finf,ignore_first_lines,dirr,prefix ):
	nuf = []
	fin = open (dirr+finf)
	infil = fin.readlines()
	fin.close()
	fout = open (dirr+prefix+finf, 'w')
	nuf =[]
	ou = -1
	for li in infil:
		ou += 1
		if ou <= ignore_first_lines: continue
		lisl  = li.split(',')
		nans = lisl.count('nan')
		nans_replaced[ou] = nans 
		infs = lisl.count('inf')
		infs_replaced[ou] = infs 
		nuli = li.replace('nan', '0.998')
		nuli = nuli.replace('inf', '1.001')
		nuf += [nuli]
	ou = -1
	for lin in nuf:
		ou += 1
		if 'validbuy' in finf:
			if ou >= line_limit_valid_buy:
				break
		if 'validsell' in finf:
			if ou >= line_limit_valid_sell:
				break
		fout.write(lin)
	fout.close()
	for ky in infs_replaced.keys():
		if infs_replaced[ky]:
			print (finf+' line '+str(ky)+' infs replaced: '+str(infs_replaced[ky]))
	for ky in nans_replaced.keys():
		if nans_replaced[ky]:
			print (finf+' line '+str(ky)+' nans replaced: '+str(nans_replaced[ky]))

def main(fins,ingnore,dirr,prefix):
	for fig in	fins:
		figx(fig,ingnore,dirr,prefix)	
