import pickle
from collections import OrderedDict
import sys
from copy import deepcopy
import os
from numpy import std, sqrt
from scipy import stats
from math import log1p
from render_app.paricmax import paricmax
spr = stats.spearmanr  # Spearman rank correlation.
from numpy import array as rayy
from numpy import log,log10
from numpy import corrcoef as corr
import struct_live
from render_app.paracor import paracor as para

class alg(object):
	def __init__(self, ob, target):
		self.targ = ob.cob.calc['targ'] = target
		self.intsperyr = 137250 * (60 / (int(ob.cob.calc['intervall'])))
		self.fields = ob.cob.calc['std_fields'].split(',')
		self.struct = struct_live.mind(ob.cob)
		self.mlt = len(self.fields)
		self.min_window = int(ob.cob.calc['min_window']) * -1
		self.menbuy = OrderedDict()
		self.mensell = OrderedDict()
		self.menhugsbuy = OrderedDict()
		self.menhugssell = OrderedDict()
		self.mentakbuy = OrderedDict()
		self.mentaksell = OrderedDict()
		self.prob_filter = float(ob.cob.calc[('prob_filter_'+target).lower()])
		self.rootbuy = ob.cob.calc[('rootbuy'+target).lower()]
		self.rootsell = ob.cob.calc[('rootbuy'+target).lower()]
		self.loadmod(ob.cob.calc[('menbuy'+target).lower()], 'buy')
		self.loadmod(ob.cob.calc[('mensell'+target).lower()], 'sell')
		if ob.cob.calc['write_adaboost'] == 'y':
				self.adafilemenb = ob.cob.pths['rpath'] + ob.cob.calc[('results_buy_'+target).lower()]
				open (self.adafilemenb, 'w')
				self.adafilemens = ob.cob.pths['rpath'] + ob.cob.calc[('results_sell_'+target).lower()]
				open (self.adafilemens, 'w')
		if ob.cob.pths['log_goin'] == 'y':
			self.goinfilerawbuy = ob.cob.pths['goin']+self.targ+ob.cob.pths['buy_prediction_input_vector_file_unordered']
			fi =open(self.goinfilerawbuy, 'w')
			fi.close()
			self.goinfilerawsell = ob.cob.pths['goin']+self.targ+ob.cob.pths['sell_prediction_input_vector_file_unordered']
			fi =open(self.goinfilerawsell, 'w')
			fi.close()
			self.goinfilebuy = ob.cob.pths['goin']+self.targ+ob.cob.pths['buy_prediction_input_vector_file_ordered']
			fi =open(self.goinfilebuy, 'w')
			fi.close()
			self.goinfilesell = ob.cob.pths['goin']+self.targ+ob.cob.pths['sell_prediction_input_vector_file_ordered']
			fi =open(self.goinfilesell, 'w')
			fi.close()

			self.buypreddex = ob.cob.pths['goin']+self.targ+ob.cob.pths['buy_pred_dex']
			fi =open(self.buypreddex, 'w')
			fi.close()
			self.sellpreddex = ob.cob.pths['goin']+self.targ+ob.cob.pths['sell_pred_dex']
			fi =open(self.sellpreddex, 'w')
			fi.close()
			self.goinfilesell = ob.cob.pths['goin']+self.targ+ob.cob.pths['sell_prediction_input_vector_file_ordered']
			fi =open(self.goinfilesell, 'w')
			fi.close()
			self.goinargrawbuy = ob.cob.pths['goin']+self.targ+ob.cob.pths['buy_prediction_arg_unordered']
			fi =open(self.goinargrawbuy, 'w')
			fi.close()
			self.goinargrawsell = ob.cob.pths['goin']+self.targ+ob.cob.pths['sell_prediction_arg_unordered']
			fi =open(self.goinargrawsell, 'w')
			fi.close()
			self.goinargbuy = ob.cob.pths['goin']+self.targ+ob.cob.pths['buy_prediction_arg_ordered']
			fi =open(self.goinargbuy, 'w')
			fi.close()
			self.goinargsell = ob.cob.pths['goin']+self.targ+ob.cob.pths['sell_prediction_arg_ordered']
			fi =open(self.goinargsell, 'w')
			fi.close()

			self.goinargdexbuy = ob.cob.pths['goin']+self.targ+ob.cob.pths['buy_prediction_arg_dex']
			fi =open(self.goinargdexbuy, 'w')
			fi.close()
			self.goinargdexsell = ob.cob.pths['goin']+self.targ+ob.cob.pths['sell_prediction_arg_dex']
			fi =open(self.goinargdexsell, 'w')
			fi.close()

			self.xraydexbuy = ob.cob.pths['goin']+self.targ+ob.cob.pths['xraydexfb']
			fi =open(self.xraydexbuy, 'w')
			fi.close()
			self.xraydexsell = ob.cob.pths['goin']+self.targ+ob.cob.pths['xraydexfs']
			fi =open(self.xraydexsell, 'w')
			fi.close()

			self.xrayfloatbuy = ob.cob.pths['goin']+self.targ+ob.cob.pths['xrayfloatfb']
			fi =open(self.xrayfloatbuy, 'w')
			fi.close()
			self.xrayfloatsell = ob.cob.pths['goin']+self.targ+ob.cob.pths['xrayfloatfs']
			fi =open(self.xrayfloatsell, 'w')
			fi.close()
			
		self.callrun(ob)
	
	def callrun (self, ob):
		while 1:
			looklist = list(ob.cob.argtuple[-1])
			lo = looklist.count(1)
			if not lo:
				continue
			else:
				b4 = 0
				while 1:
					looklist = list(ob.cob.argtuple[-1]) # The last shared array is 'timing'
					looklist.reverse()
					baklo = looklist.index(1)
					endd = len(looklist) - baklo
					if b4 == 0:
						self.first = int(ob.cob.argtuple[-1][0])
						b4 = endd
					if b4 >= endd:
						continue
					print('first interval ',self.first)
					print(b4, endd, 'strun_live.py for:'+ self.targ+' now treating these intervals')
					self.runn(ob, b4, endd)
					b4 = endd

	def runn(self, ob, bg, endd):
		for mimf in range(bg,endd):
			self.callvol_live(ob, self.struct.calcl, ob.clo, ob.cob.argtuple, ob.cob.avg_symbs, mimf)
			self.gamut_diff_live(ob, self.struct.calcl, ob.clo, ob.cob.argtuple, 'f20', ob.cob.avg_symbs, mimf)
			self.gamut_diff_live(ob, self.struct.calcl, ob.clo, ob.cob.argtuple, 'f40', ob.cob.avg_symbs, mimf)
			self.gamut_corr_live(ob,self.struct.calcl, ob.clo, ob.cob.argtuple, 'cor_roots', 'tick_cor',self.struct.focii['tick_sec'],ob.cob.avg_symbs, mimf)
			self.gamut_corr_live(ob,self.struct.calcl, ob.clo, ob.cob.argtuple, 'cor_roots', 'dex_cor',self.struct.focii['dex_sec'],ob.cob.avg_symbs, mimf)
			self.gamut_corr_live(ob,self.struct.calcl, ob.clo, ob.cob.argtuple, 'cryp_cors', 'cry_tick',self.struct.focii['crypto_tick_sec'],ob.cob.avg_symbs, mimf)
			self.gamut_corr_live(ob,self.struct.calcl, ob.clo, ob.cob.argtuple, 'cryp_cors', 'cry_dex',self.struct.focii['crypto_dex_sec'],ob.cob.avg_symbs, mimf)
			self.gamut_para_live(ob, self.struct.calcl, ob.clo, ob.cob.argtuple, ob.cob.avg_symbs, mimf)
			self.gamut_spear_live(ob, self.struct.calcl, ob.clo,  ob.cob.argtuple, 'tick_cor_spear',
								self.struct.focii['tick_sec'], ob.cob.avg_symbs ,mimf)
			self.gamut_spear_live(ob, self.struct.calcl, ob.clo, ob.cob.argtuple, 'dex_cor_spear',
									self.struct.focii['dex_sec'], ob.cob.avg_symbs, mimf)
			self.gamut_prab_live(ob, self.struct.calcl, ob.clo, ob.cob.argtuple, 'f20', ob.cob.avg_symbs, mimf)
			self.gamut_prab_live(ob, self.struct.calcl, ob.clo, ob.cob.argtuple, 'f40', ob.cob.avg_symbs, mimf)
			self.callcdeclinea_live(ob, self.struct.calcl, ob.clo, ob.cob.argtuple, ob.cob.avg_symbs, mimf)
			self.gamut_logg_live(ob, self.struct.calcl, ob.clo, ob.cob.argtuple, ob.cob.avg_symbs, mimf)
			self.execmbuy(ob,  self.struct.calcl, [mimf])
			self.execmsell(ob,  self.struct.calcl, [mimf])

	def joinlint(self, li):
		slist = []
		for x in li:
			slist += [int(x)]
		return slist

	def column(self, matrix, i):
		return [row[i] for row in matrix]

	def joinl(self, li):
		slist = []
		for x in li:
			slist += [str(x)]
		jlist = ','.join(slist)
		jlist = jlist.replace('-inf', '-3')
		jlist = jlist.replace('inf', '3')
		jlist = jlist.replace('nan', '1.0003')
		jlist = jlist.split(',')
		retlist = []
		for s in jlist:
			retlist += [float(s)]
		return retlist

	def sort_args(self, goin, argorder):
		nugoin = []
		for x in argorder:
			nugoin += [goin[x]]
		return nugoin

	def wr_line(self, fi, linee):
		linee = linee.replace('[','')
		linee = linee.replace(']','')
		fout = open(fi, 'a')
		fout.write(linee+'\n')
		fout.close()

	def execmbuy(self, ob, mat, spot):
		for mimf in spot:
			self.goinraw = deepcopy(self.column(mat,mimf)[:ob.last_calc_int+1])
			self.goin = self.joinl(self.goinraw)
			if ob.cob.pths['log_goin'] == 'y':
				self.wr_line(self.goinfilerawbuy, str(self.goinraw))
				# The argument order of the first prediction module, disregarding the
				# tak variable is used as an example. This will likely be the same
				# for all prediction modules.
				self.wr_line(self.goinfilebuy, str(self.sort_args(self.goin, self.menhugsbuy[0])))
				self.wr_line(self.buypreddex, str(self.menhugsbuy[0]))
				self.wr_line(self.goinargrawbuy, str(list(range(len(self.goinraw)))))
			sum_men = 0
			if ob.cob.calc['write_adaboost'] == 'y':
				fout = open(self.adafilemenb, 'a')
			for   cou, ky in enumerate(list(self.menbuy.keys())):
				# Put the input data in the list goin into
				# the correct sequence
				nugoin = self.sort_args(self.goin, self.menhugsbuy[ky])
				if ob.cob.pths['log_goin'] == 'y':
					self.wr_line(self.goinargbuy, str(nugoin))
					self.wr_line(self.goinargdexbuy, str(self.menhugsbuy[ky]))
				xray = rayy(nugoin[-1 * self.mentakbuy[ky]:])
				if ob.cob.pths['log_goin'] == 'y':
					self.wr_line(self.xraydexbuy, str(self.menhugsbuy[ky][-1 * self.mentakbuy[ky]:]))
					self.wr_line(self.xrayfloatbuy, str(list(xray)))
				xray = xray.reshape(1, -1)  # if it contains a single sample.
				val = self.menbuy[ky].predict(xray)[0]
				prob = self.menbuy[ky].predict_proba(xray)[0]
				if ob.cob.calc['write_adaboost'] == 'y':
					if val == -1 and prob[0] >= self.prob_filter:
						fout.write(str(cou) + ',')
				if val == -1:
					sum_men += 1
			if ob.cob.calc['write_adaboost'] == 'y':
				fout.write(str(sum_men)+'\n')
				fout.close()

	def execmsell(self, ob, mat, spot):
		for mimf in spot:
			self.goinraw = deepcopy(self.column(mat,mimf)[:ob.last_calc_int+1])
			self.goin = self.joinl(self.goinraw)
			if ob.cob.pths['log_goin'] == 'y':
				self.wr_line(self.goinfilerawsell, str(self.goinraw))
				# The argument order of the first prediction module, disregarding the
				# tak variable is used as an example. This will likely be the same
				# for all prediction modules.
				self.wr_line(self.goinfilesell, str(self.sort_args(self.goin, self.menhugssell[0])))
				self.wr_line(self.sellpreddex, str(self.menhugssell[0]))				
				self.wr_line(self.goinargrawsell, str(list(range(len(self.goinraw)))))
			sum_men = 0
			if ob.cob.calc['write_adaboost'] == 'y':
				fout = open(self.adafilemens, 'a')
			for cou, ky in enumerate(list(self.mensell.keys())):
				# Put the input data in the list goin into
				# the correct sequence.
				nugoin = self.sort_args(self.goin, self.menhugssell[ky])
				if ob.cob.pths['log_goin'] == 'y':
					self.wr_line(self.goinargsell, str(nugoin))
					self.wr_line(self.goinargdexsell, str(self.menhugssell[ky]))
				xray = rayy(nugoin[-1 * self.mentaksell[ky]:])
				if ob.cob.pths['log_goin'] == 'y':
					self.wr_line(self.xraydexsell, str(self.menhugssell[ky][-1 * self.mentaksell[ky]:]))
					self.wr_line(self.xrayfloatsell, str(list(xray)))
				xray = xray.reshape(1, -1)  # if it contains a single sample.
				val = self.mensell[ky].predict(xray)[0]
				prob = self.mensell[ky].predict_proba(xray)[0]
				if ob.cob.calc['write_adaboost'] == 'y':
					if val == -1 and prob[0] >= self.prob_filter:
						fout.write(str(cou) + ',')
				if val == -1:
					sum_men += 1
			if ob.cob.calc['write_adaboost'] == 'y':
				fout.write(str(sum_men)+'\n')
				fout.close()


	def loadmod(self, fil, bos):
		if bos == 'buy':
			secroot = self.rootbuy
			gdic = self.menbuy
			hdic = self.menhugsbuy
			takdic = self.mentakbuy
		else:
			secroot = self.rootsell
			gdic = self.mensell
			hdic = self.menhugssell
			takdic = self.mentaksell
		fin = open(fil)
		lins = fin.readlines()
		for i, li in enumerate(lins):
			lis = li.split(',')
			with open(secroot + lis[16], 'rb') as handle:
				gdic[i] = pickle.load(handle)
			hdic[i] = self.joinlint(lis[17:])
			takdic[i] = int(lis[13])

	def callvol_live(self, ob, targ, clo, rays, varss, mimf):
		bakk= - self.min_window # Because the data window prior
		# to the opening value is filled with either data from
		# a prior day or a Brownian bridge, bakk + mimf
		# should never be before self.first.
		if bakk + mimf < self.first: return
		bak = -1 * mimf
		if abs(bak) > int(ob.cob.calc['window']):
			bak = -1 * int(ob.cob.calc['window'])
		bak = bak * self.mlt
		for sy in varss:
			fyh = rays[ob.cob.vlo[sy + 'flat']][bak+mimf*self.mlt:mimf*self.mlt]
			targ[clo['volatility_vola_'+sy]][mimf] = self.compvol(fyh, self.intsperyr)

	def gamut_diff_live(self, ob, targ, clo, rays, oss, varss, mimf):
		bakk =  self.min_window
		if bakk + mimf < self.first: return
		if '20' in oss:
			bak = -20
		if '40' in oss:
			bak = -40
		#if mimf - abs(bak) < self.first:
			#bak = -1 * mimf
		bak = bak * self.mlt
		flo = mimf * self.mlt
		for sy in varss:
			targ[clo['diffs_'+oss+'_'+sy]][mimf] = paricmax(rays[ob.cob.vlo[ob.cob.calc['targ']+'flat']][bak + flo:flo]) - \
													paricmax(rays[ob.cob.vlo[sy + 'flat']][bak + flo:flo])

	def gamut_corr_live(self, ob, targ, clo, rays, topkey, oss, tick_sec, varss, mimf):
		bakk = self.min_window
		if bakk + mimf < self.first: return
		bak = -1 * mimf
		if abs(bak) > int(ob.cob.calc['window']):
			bak = -1 * int(ob.cob.calc['window'])
		bak = bak * self.mlt
		flo = mimf * self.mlt
		for sy in varss:
			targ[clo[topkey+'_'+ oss + '_' + sy]][mimf] = \
				corr(rays[ob.cob.vlo[tick_sec + 'flat']][bak+flo:flo], rays[ob.cob.vlo[sy + 'flat']][bak + flo:flo])[0, 1]

	def gamut_para_live(self, ob, targ, clo, rays, varss, mimf):
		bakk = self.min_window
		if bakk +  mimf < self.first: return
		bak = -1 * mimf
		if abs(bak) > int(ob.cob.calc['window']):
			bak = -1 * int(ob.cob.calc['window'])
		bak = bak * self.mlt
		flo = mimf * self.mlt
		for sy in varss:
			a, bixcc, c, d, e, inflect = para(rayy(rays[ob.cob.vlo[ob.cob.calc['targ'] + 'flat']][bak + flo:flo]), rayy(rays[ob.cob.vlo[sy + 'flat']][bak + flo:flo]))
			targ[clo['outfi_para_roots_ixcc_' + sy]][mimf] = self.loglog(bixcc)

	def gamut_spear_live (self, ob, targ, clo, rays, oss, tick_sec, varss, mimf):
		bakk = self.min_window
		if bakk + mimf < self.first: return
		bak = -1 * mimf
		if abs(bak) > int(ob.cob.calc['window']):
			bak = -1 * int(ob.cob.calc['window'])
		bak = bak * self.mlt
		flo = mimf * self.mlt
		if 'dex' in oss:
			pvoss = 'dex_cor_pvalue'
		else:
			pvoss = 'tick_cor_pvalue'
		for sy in varss:
			targ[clo['spear_roots_' + oss + '_' + sy]][mimf], targ[clo['pvalue_' + pvoss + '_' + sy]][mimf] = spr(
				rays[ob.cob.vlo[tick_sec + 'flat']][bak + flo:flo], rays[ob.cob.vlo[sy + 'flat']][bak + flo:flo])

	def gamut_prab_live(self, ob, targ, clo, rays, oss, varss, mimf):
		bakk =  self.min_window
		if bakk + mimf < self.first: return
		if '20' in oss:
			bak = -20
		if '40' in oss:
			bak = -40
		#if mimf - abs(bak) < self.first:
			#bak = -1 * mimf
		bak = bak * self.mlt
		flo = mimf * self.mlt
		for sy in varss:
				targ[clo['prab_'+oss+'_'+sy]][mimf] = paricmax(rays[ob.cob.vlo[sy + 'flat']][bak + flo:flo])

	def callcdeclinea_live(self, ob, targ, clo, rays, varss, mimf ):
		for sy in varss:
			qray = self.quarter(list(rays[ob.cob.vlo[sy + 'flat']][self.first* self.mlt:mimf* self.mlt+1]))
			qray = self.cdeclinea(qray)
			targ[clo['decline_cline_'+sy]][mimf] = qray[-1]

	def gamut_logg_live(self, ob, targ, clo, rays, varss, mimf):
		lo = mimf * self.mlt
		for sy in varss:
			targ[clo['log10_log_' + sy]][mimf] = self.loglog(rays[ob.cob.vlo[sy + 'flat']][lo])

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


if __name__ == "__main__":
	import nov_admin
	import fig
	import struct_calc
	obb = fig.par()
	obb.add_list('conflate', obb.tre['conflate_fullx'])
	obb.add_list('conflate_fill', obb.tre['conflate_fillx'])
	obx = nov_admin.symb(obb)
	tg = 'MSFT'
	print (obx.calc[('results_buy_'+tg).lower()])
	sys.exit()
	# Test the dictionary holding the list of beginning/end datetime pairs for
	# each training day
	print (obx.rdi['train']['dates'])
	# struct_calc.calk will write a file containing the 
	# column names for the training and validation csv files
	# in the labels folder if the second parameter is True.
	ob = struct_calc.calk(obx, True)
