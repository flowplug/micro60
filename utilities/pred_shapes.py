import fig

obb=fig.par()
obb.add_list('fullntargs',obb.tre['fullntargs'])

outfile = open(obb.pths['label_dir'] + obb.pths['curp']+'/'+ obb.pths['pred_shape_file'],'w')

for ticker in obb.fullntargs:
	readfile = open(obb.calc['menbuy'+ticker.lower()])
	lisof = readfile.readlines()
	outfile.write(ticker+' buy entries: '+str(len(lisof))+'\n')
	readfile.close()
	readfile = open(obb.calc['mensell'+ticker.lower()])
	lisof = readfile.readlines()
	outfile.write(ticker+' sell entries: '+str(len(lisof))+'\n')
	readfile.close()
print ('Shapes written at '+obb.pths['label_dir'] + obb.pths['curp']+'/'+ obb.pths['pred_shape_file'])	
