import struct_hist
import pickle
import sys
from numpy import std, sqrt
from scipy import stats
from math import log1p
from render_app.paricmax import paricmax
spr = stats.spearmanr  # Spearman rank correlation.
from numpy import log10
from numpy import corrcoef as corr
from render_app.paracor import paracor as para

class alg(object):
	def __init__(self, ob, target):
		ob.cob.calc['targ'] = target
		self.min_window = int(ob.cob.calc['min_window'])
		self.intsperyr = 137250 * (60 / (int(ob.cob.calc['intervall'])))
		self.fields = ob.cob.calc['std_fields'].split(',')
		self.lenfields = len(self.fields)		
		doval = False
		dotrain = False
		if ob.cob.calc['validate'] == 'y':
			doval = True
			self.rangv = range(len(ob.cob.rdi['valid']['dtrue']))
		if ob.cob.calc['train'] == 'y':
			dotrain = True
			self.rangt = range(len(ob.cob.rdi['train']['dtrue']))
		self.structh = struct_hist.mind(ob, dotrain, doval)
		self.ray_dict = {}
		for ky in ob.cob.rdi.keys():
			if ob.cob.rdi[ky] == {}: 
				continue
			# Load the pickled arrays
			path = ob.cob.pths['pickle_dir']+ob.cob.pths['curp']+'/'+ky+'.pickle'
			handle = open(path, 'rb')
			self.ray_dict[ky] = pickle.load(handle)
		self.runn(ob)
		
	def runn(self, ob):
		self.mlt = self.lenfields
		self.callvol_hist(ob, 'train', self.structh.calct, ob.clo, self.ray_dict['train'], ob.cob.avg_symbs)
		self.callvol_hist(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], ob.cob.avg_symbs)
		print ('volatility done')
		self.gamut_diff(ob, 'train', self.structh.calct, ob.clo, self.ray_dict['train'], 'f20', ob.cob.avg_symbs)
		self.gamut_diff(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], 'f40', ob.cob.avg_symbs)
		self.gamut_diff(ob, 'train', self.structh.calct, ob.clo, self.ray_dict['train'], 'f40', ob.cob.avg_symbs)
		self.gamut_diff(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], 'f20', ob.cob.avg_symbs)
		print ('diffs done')
		self.gamut_corr(ob, 'train', self.structh.calct, ob.clo, self.ray_dict['train'], 'cor_roots', 'tick_cor',self.structh.focii['tick_sec'],ob.cob.avg_symbs)
		self.gamut_corr(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], 'cor_roots', 'tick_cor',self.structh.focii['tick_sec'],ob.cob.avg_symbs)
		self.gamut_corr(ob, 'train', self.structh.calct, ob.clo, self.ray_dict['train'], 'cor_roots', 'dex_cor',self.structh.focii['dex_sec'],ob.cob.avg_symbs)
		self.gamut_corr(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], 'cor_roots', 'dex_cor',self.structh.focii['dex_sec'],ob.cob.avg_symbs)
		self.gamut_corr(ob, 'train', self.structh.calct, ob.clo, self.ray_dict['train'], 'cryp_cors', 'cry_tick',self.structh.focii['crypto_tick_sec'],ob.cob.avg_symbs)
		self.gamut_corr(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], 'cryp_cors', 'cry_tick',self.structh.focii['crypto_tick_sec'],ob.cob.avg_symbs)
		self.gamut_corr(ob, 'train', self.structh.calct, ob.clo, self.ray_dict['train'], 'cryp_cors', 'cry_dex',self.structh.focii['crypto_dex_sec'],ob.cob.avg_symbs)
		self.gamut_corr(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], 'cryp_cors', 'cry_dex',self.structh.focii['crypto_dex_sec'],ob.cob.avg_symbs)
		print ('corrs done')
		self.gamut_para(ob, 'train', self.structh.calct, ob.clo, self.ray_dict['train'], 'ixcc', ob.cob.avg_symbs)
		self.gamut_para(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], 'ixcc', ob.cob.avg_symbs)
		print ('paras done')
		self.gamut_spear(ob, 'train', self.structh.calct, ob.clo, self.ray_dict['train'], 'tick_cor_spear',self.structh.focii['tick_sec'], ob.cob.avg_symbs)
		self.gamut_spear(ob, 'train', self.structh.calct, ob.clo, self.ray_dict['train'], 'dex_cor_spear',self.structh.focii['dex_sec'], ob.cob.avg_symbs)
		self.gamut_spear(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], 'tick_cor_spear',self.structh.focii['tick_sec'], ob.cob.avg_symbs)
		self.gamut_spear(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], 'dex_cor_spear',self.structh.focii['dex_sec'], ob.cob.avg_symbs)
		print ('spears_done')
		self.gamut_prab(ob, 'train', self.structh.calct, ob.clo, self.ray_dict['train'], 'f20', ob.cob.avg_symbs)
		self.gamut_prab(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], 'f20', ob.cob.avg_symbs)
		self.gamut_prab(ob, 'train', self.structh.calct, ob.clo, self.ray_dict['train'], 'f40', ob.cob.avg_symbs)
		self.gamut_prab(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], 'f40', ob.cob.avg_symbs)
		print ('prabs done')
		if ob.cob.calc['decline'] == 'y':
			self.callcdeclinea( self.structh.calct, ob.clo, self.ray_dict['train'], ob.cob.avg_symbs)
			self.callcdeclinea( self.structh.calcv, ob.clo, self.ray_dict['valid'], ob.cob.avg_symbs)
		print ("decline done")
		self.gamut_logg(ob, 'train',self.structh.calct, ob.clo, self.ray_dict['train'], ob.cob.avg_symbs)
		self.gamut_logg(ob, 'valid', self.structh.calcv, ob.clo, self.ray_dict['valid'], ob.cob.avg_symbs)
		
		# Write the training and validation data to .csv files.
		self.structh.put_fis_hist(ob.cob, 'train', self.ray_dict['train'])
		self.structh.put_fis_hist(ob.cob, 'valid', self.ray_dict['valid'])
		print('done')

	def loglog(self, val):
		neg = False
		skip = False
		if val < 0:
			val = val * -1
			neg = True
		if val == 1.0:
			skip = True
			vallog = .0013
		if val == 0.0:
			skip = True
			vallog = -2.6
		if str(val) == 'nan':
			vallog = .0013
			skip = True
		if 'inf' in str(val):
			vallog = 3.0
			skip = True
		if not skip:
			vallog = log10(float(val))
			if neg: vallog = -1 * vallog
		return vallog

	def cdeclinea(self, sray):
		# For the price array passed in sray,
		# start a list t with initial value 0.
		# The t list will end up the same length
		# as sray because we start a for loop
		# traversing sray at the second value
		# (the first value is index 0, the second
		# is 1, which is used below.). If suceeding
		# values are greater than the one before,
		# increment the prior value of t by 0.01.
		# If less, decrement by 0.1. 
		it = 0
		vdwn = 0
		vup = 0
		m = sray[0]
		t = [0]
		for x in sray[1:]:
			if x > m:
				vup += .01
				vdwn = 0
				it = vup
			if x < m:
				vdwn -= .01
				vup = 0
				it = vdwn
			t += [it]
			m = x
		return t

	def quarter(self, ray):
		ot = []
		for lo in range(3, len(ray), 4):
			ot += [ray[lo]]
		return ot


	def callcdeclinea(self, targ, clo, rays, varss):
		for sy in varss:
			# Quarter takes every fourth value, which will be the closing value
			# for the interval.
			qray = self.quarter(list(rays[sy]))
			qray = self.cdeclinea(qray)
			for i, x in enumerate(qray):
				try:
					targ[clo['decline_cline_'+sy]][i] = x
				except:
					pass

	def gamut_prab(self, ob, suite, targ, clo, ray_dict, oss, varss):
		bakk = -1 * self.min_window
		for sy in varss:
			for lo in range(len(ob.cob.rdi[suite]['dtrue'])):
				if bakk + lo < 0: continue
				flo = lo * self.lenfields
				if '20' in oss:
					wvlen = 20
					if (-20 + lo) < 0:
						wvlen = lo
				if '40' in oss:
					wvlen = 40
					if (-40 + lo) < 0:
						wvlen = lo
				wvlen = self.lenfields * wvlen
				bak = wvlen * -1
				if abs(bak) > flo:
					bak = -1*flo
				targ[clo['prab_'+oss+'_'+sy]][lo] = paricmax(ray_dict[sy][bak + flo:flo])


				
	def gamut_spear(self, ob, suite, targ, clo, ray_dict, oss, tick_sec, varss):
		bakk = -1 * self.min_window
		for sy in varss:
			for lo in range(len(ob.cob.rdi[suite]['dtrue'])):
				if bakk + lo < 0: continue
				bak = -1* int(ob.cob.calc['window'])
				flo = lo * self.lenfields  # +
				bak = bak * self.lenfields
				if abs(bak) >= flo:
					bak = -1*flo
				if 'dex' in oss:
					pvoss = 'dex_cor_pvalue'
				else:
					pvoss = 'tick_cor_pvalue'
				# spr returns two values, a correlation c, -1 > c < 1.
				# Secondly a pvalue, p < = 100%,  the small the better the associated pvalue to the spearman correlation.
				targ[clo['spear_roots_'+oss+'_' + sy]][lo], targ[clo['pvalue_'+pvoss+'_' + sy]][lo] = spr(ray_dict[tick_sec][bak + flo:flo], ray_dict[sy][bak + flo:flo])

	def gamut_para(self, ob, suite, targ, clo, ray_dict, oss, varss):
		bakk = -1 * self.min_window
		for sy in varss:
			for lo in range(len(ob.cob.rdi[suite]['dtrue'])):
				if bakk + lo < 0:
					continue
				bak = -1* int(ob.cob.calc['window'])
				flo = lo * self.lenfields  # +
				bak = bak * self.lenfields
				if abs(bak) > flo:
					bak = -1*flo
				a, bixcc, c, d, e, inflect = para(ray_dict[ob.cob.calc['targ']][bak + flo:flo], ray_dict[sy][bak + flo:flo])
				targ[clo['outfi_para_roots_' + oss + '_' + sy]][lo] = self.loglog(bixcc)

	def gamut_corr(self, ob, suite, targ, clo, ray_dict, topkey, oss, tick_sec, varss):
		bakk = -1 * self.min_window
		for sy in varss:
			for lo in range(len(ob.cob.rdi[suite]['dtrue'])):
				if bakk + lo < 0: continue
				bak = -1 * int(ob.cob.calc['window'])
				flo = lo * self.lenfields
				if abs(bak) > flo:
					bak = -1 * flo
				targ[clo[topkey+'_'+ oss + '_' + sy]][lo] = corr(ray_dict[tick_sec][bak+flo:flo], ray_dict[sy][bak + flo:flo])[0, 1]

	def gamut_diff(self, ob, suite, targ, clo, ray_dict, oss, varss):
		bakk = -1 * self.min_window
		for sy in varss:
			for lo in range(len(ob.cob.rdi[suite]['dtrue'])):
				if bakk + lo < 0: continue
				flo = lo * self.lenfields
				if '20' in oss:
					bak = 20
				if '40' in oss:
					bak = 40
				#bak = self.lenfields * wvlen
				bak = bak* -1 * self.lenfields
				if abs(bak) > flo:
					bak = -1*flo
				targ[clo['diffs_'+oss+'_'+sy]][lo]  = paricmax(ray_dict[ob.cob.calc['targ']][bak + flo:flo]) - paricmax(ray_dict[sy][bak + flo:flo])

	def compvol(self, ray, fc):
		vls = []
		for x in range(1, len(ray)):
			try:
				if ray[x - 1] != 0:
					vls += [log1p(ray[x] / ray[x - 1])]
				else:
					vls += [0]
			except:
				pass
		return std(vls) * (sqrt(fc))

	def callvol_hist(self,ob, suite, targ, clo, ray_dict, varss):
		for sy in varss:
			bakk = -1 * self.min_window
			#print (suite,len(ob.cob.rdi[suite]['dtrue']))
			for lo in range(len(ob.cob.rdi[suite]['dtrue'])):
				if bakk + lo < 0: continue
				bak = -1*lo
				if abs(bak) > int(ob.cob.calc['window']):
					bak  =  -1 * int(ob.cob.calc['window'])
				#if lo == 100:
					#fyhh = list(ray_dict[sy][:])
					#print (sy, fyhh.count(0.0))
				fyh = ray_dict[sy][bak + lo:lo]
				targ[clo['volatility_vola_'+sy]][lo] = self.compvol(fyh, self.intsperyr)
		#sys.exit()	
	def gamut_logg(self, ob, suite, targ, clo, ray_dict, varss):
		for sy in varss:
			for lo in range(len(ob.cob.rdi[suite]['dtrue'])):
				targ[clo['log10_log_' + sy]][lo] = self.loglog(ray_dict[sy][lo])
				

if __name__ == "__main__":
	import nov_admin
	import fig
	import struct_calc
	obb = fig.par()
	obb.add_list('conflate', obb.tre['conflate_fullx'])
	obb.add_list('conflate_fill', obb.tre['conflate_fillx'])
	obx = nov_admin.symb(obb)
	# Test the dictionary holding the list of beginning/end datetime pairs for
	# each training day
	print (obx.rdi['train']['dates'])
	# struct_calc.calk will write a file containing the 
	# column names for the training and validation csv files
	# in the labels folder.
	ob = struct_calc.calk(obx)
