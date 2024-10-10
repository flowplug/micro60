from collections import OrderedDict
from numpy import zeros
import sys
import os

class calk(object):
	def __init__(self, ob, print_series = False):
		path = ob.pths['label_dir']+ob.pths['curp']
		isExist =os.path.exists(path)
		if not isExist:
			os.makedirs(path)
		self.series_name_file = path + '/'+ob.calc['column_names_file']
		self.intsperyr = 137250 * (60 / (int(ob.calc['intervall'])))
		self.geis = OrderedDict()
		self.geis['volatility'] = ['vola']
		self.geis['diffs'] = ['f20', 'f40']
		self.geis['cor_roots'] = ['tick_cor', 'dex_cor']
		self.geis['cryp_cors'] = ['cry_tick', 'cry_dex']
		self.geis['outfi_para_roots'] = ['ixcc']
		self.geis['spear_roots'] = ['tick_cor_spear', 'dex_cor_spear']
		self.geis['pvalue'] = ['tick_cor_pvalue', 'dex_cor_pvalue']
		self.geis['diffs'] = ['f20', 'f40']
		self.geis['prab'] =['f20', 'f40']
		self.geis['decline'] = ['cline']
		self.geis['log10'] = ['log']
		# Place the needed floating arrays within the above dictionary structure.
		self.gos = self.init_geist(ob)

		self.series_names, self.clo, self.last_calc_int, self.after_buy_int = self.parse_series_names(ob)
		ob.last_calc_int = self.last_calc_int
		self.cob = ob
		if ob.calc['print_series_names'] == 'y' and print_series:
			self.print_series()

	def print_series(self):
		fout = open (self.series_name_file, 'w')
		for lo,ky in enumerate(list(self.series_names.keys())):
			fout.write(str(lo)+','+self.series_names[ky]+'\n')

	def	parse_series_names(self,ob):
		# The series names will be the same for
		# any of the possible three top key
		# values of self.master: valid, train, or live.
		# we therefore search for first available.
		for ky in ob.rdi.keys():
			if ob.rdi[ky] == {}:
				continue
			clo = OrderedDict()
			series_names = OrderedDict()
			ou = -1
			for kyy in self.gos[ky].keys():
				for tag in self.gos[ky][kyy].keys():
					if 'numpy.ndarray' in str(type(self.gos[ky][kyy][tag])):
						ou += 1
						series_names[ou] = kyy + '_' + tag
						clo[series_names[ou]] = ou
						continue
					else:
						for inner_tag in self.gos[ky][kyy][tag].keys():
							ou += 1
							series_names[ou] = kyy+'_'+tag+'_'+inner_tag
							clo[series_names[ou]] = ou
			return series_names, clo, clo[ob.calc['last_calc_field']], 0

	def fillraydict(self, ob, ky):
		intervals = len(ob.rdi[ky]['dtrue'])
		return zeros((intervals))

	def init_geist(self, ob):
		master ={}
		for kz in ob.rdi.keys():
			if ob.rdi[kz] == {}: 
				continue
			nugeis ={}
			for ky in self.geis.keys():
				nugeis[ky] ={}
				for tag in self.geis[ky]:
					nugeis[ky][tag] = {}
					for sy in ob.avg_symbs:
						nugeis[ky][tag][sy] = self.fillraydict(ob,kz)
			master[kz] = nugeis
		return master
	
if __name__ == "__main__":
	import nov_admin
	import fig
	obb = fig.par()
	obb.add_list('conflate', obb.tre['conflate_fulln'])
	obb.add_list('conflate_fill', obb.tre['conflate_fill'])
	obx = nov_admin.symb(obb)
	obx.cob=obx
	aa = calk(obx)



