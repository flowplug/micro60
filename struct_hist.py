
import sys
import os
import kspo
from copy import deepcopy
from numpy import zeros

loaddict = False
class mind(object):
	def __init__(self, ob, init_train, init_valid):
		path = ob.cob.pths['label_dir']+'/'+ob.cob.pths['curp']+ob.cob.calc['train_targ']
		isExist =os.path.exists(path)
		if not isExist:
			os.makedirs(path)     
		self.ks = kspo.loc()
		self.calct = zeros((len(ob.series_names.keys()),len(ob.cob.rdi['train']['dtrue'])))
		self.calcv = zeros((len(ob.series_names.keys()), len(ob.cob.rdi['valid']['dtrue'])))
		self.varss = ob.cob.avg_symbs
		self.ldir = path+'/'

		if init_train:
			flist = ['trainbuy.csv', 'trainsell.csv']
			for fl in flist:
				fj = open(self.ldir +fl, 'w')
				fj.close()
		if init_valid:
			flist = ['validbuy.csv', 'validsell.csv']
			for fl in flist:
				fj = open(self.ldir + fl, 'w')
				fj.close()
		self.focii = self.read_focii(ob)
		
	def read_focii(self,ob):
		focii = {}
		focii['tick_sec'] = ob.cob.calc['tick_sec'].upper()
		focii['dex_sec'] = ob.cob.calc['dex_sec'].upper()
		focii['crypto_tick_sec'] = ob.cob.calc['crypto_tick_sec'].upper()
		focii['crypto_dex_sec'] = ob.cob.calc['crypto_dex_sec'].upper()
		return focii

	def column(self, matrix, i):
		return [row[i] for row in matrix]

	def quarter(self, ray):
		ot = []
		for lo in range(0, len(ray), 4):
			ot += [ray[lo]]
		return ot

	def put_fis_hist(self, ob, suite, ray_dict, tag=''):
		targ = ob.calc['targ'].upper()
		targray = deepcopy(ray_dict[targ])
		if tag == '':
			if suite == 'train':
				mat = self.calct
			if suite == 'valid':
				mat = self.calcv
		if tag == '':
			buyr, sellr = self.ks.main(self.quarter(list(targray)))

		for wrs in [ 'buy', 'sell']:
			if wrs == 'buy':
				bos = buyr
			if wrs == 'sell':
				bos = sellr
			f = open(self.ldir + suite + wrs + tag+'.csv', 'w')
			for xx in range(mat.shape[1]):
				col = self.column(mat,xx)
				for val in col:
					f.write(str(val)+',')
				f.write(str(bos[xx])+'\n')
			f.close()







