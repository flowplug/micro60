import os
import sys
from operator import itemgetter
import figsim
from numpy import zeros, transpose
from numpy import array as rayy
from collections import OrderedDict
import pickle
import datetime as dt
from statistics import mean
import nov_admin
from copy import deepcopy
import struct_calc

class sim_mat(object):
	def __init__(self, dirr):
		self.dirr = dirr
		self.bos = ['buy.csv', 'sell.csv']
		for bs in self.bos:
			if 'buy' in bs:
				self.matbuy = transpose(self.readft(self.dirr+"aaavalid"+bs))
			else:
				self.matsell = transpose(self.readft(self.dirr+"aaavalid"+bs))
		#return self.matbuy, self.matsell
	
	def readft(self,fin):
		finh = open(fin)
		lins = finh.readlines()
		rows = len(lins)
		samp = deepcopy(lins[0])
		samp = samp.replace('\n','')
		tak = len(samp.split(',')) - 1 # Last column is target.
		mat = zeros((rows,tak))
		cou = -1
		for lin in lins:
			lin = lin.replace('\n','')
			cou+=1
			ist = lin.split(',')
			ist = ist[:-1] # The last value is the target and is eliminated, as it was in scikit.py
			ou = -1
			for lo in range(mat.shape[1]):
				ou += 1
				mat [cou][ou] = float(ist[lo])
		return mat

class tran(object):
	def __init__(self, bos, interv, datetime, price, shares, openorclose, shortorlong):
		self.bos = bos
		self.iterv = interv
		self.dtime = datetime
		self.price = price
		self.shares = shares
		self.openorclose = openorclose
		self.shortorlong = shortorlong

class itvstruct(object):
	def __init__(self, itvl):
		self.itvl = 0
		self.bpredmods = []
		self.b_prob_neg_ones = []
		self.b_prob_pos_ones = []
		self.spredmods = []
		self.s_prob_neg_ones = []
		self.s_prob_pos_ones = []
		self.pricetarg = 0
		self.prtick_nasd = 0
		self.prtick_nyse = 0
		self.targ_cor_nysetick = 0

class signal(object):
	def __init__(self, lint):
		self.sigdic = {}
		for xx in range(lint):
			self.sigdic[xx]={}
			self.sigdic[xx]['itvfired'] =[]
			#self.sigdic[xx]['dtstamp'] =[]
			self.sigdic[xx]['prob_neg_one'] =[]
			self.sigdic[xx]['prob_pos_one'] =[]


class simu(object):
	def __init__(self, ob):
		self.target = target = ob.calc['sim_targ']
		self.inpath = ob.pths['label_dir']+ob.pths['sim_curp']+ob.calc['sim_targ']+'/'
		jjj = sim_mat(self.inpath)
		self.matbuy = jjj.matbuy
		self.matsell = jjj.matsell
		self.prices = self.fillraydict(ob,'valid')
		self.initialbal = float(ob.calc['initial_balance'])
		self.currentbal = float(ob.calc['initial_balance'])
		self.seelist = 'seelist.csv'
		self.tranlist = []
		isExist =os.path.exists(ob.pths['simfolder'])
		if not isExist:
			os.makedirs(ob.pths['simfolder'])
		ct = dt.datetime.now()
		daystr = dt.datetime.today().strftime('%Y-%m-%d')
		# Use timestamp of current time to create a unique folder for simulation information.
		fol = ob.pths['simfolder']+'/'+daystr+'f'+str(ct.timestamp()).replace('.','_')+'/'
		os.makedirs(fol)
		ob.pths['lpath'] = fol
		self.menbuy = OrderedDict()
		self.mensell = OrderedDict()
		self.menhugsbuy = OrderedDict()
		self.menhugssell = OrderedDict()
		self.mentakbuy = OrderedDict()
		self.mentaksell = OrderedDict()
		self.prob_filter = float(ob.calc[('prob_filter_'+target).lower()])
		self.rootbuy = ob.calc[('rootbuy'+target).lower()]
		self.rootsell = ob.calc[('rootbuy'+target).lower()]
		self.loadmod(ob.calc[('menbuy'+target).lower()], 'buy')
		self.loadmod(ob.calc[('mensell'+target).lower()], 'sell')
		self.skip = int(ob.calc['fins_ignore'])
		self.dtrue = ob.rdi['valid']['dtrue'][self.skip+1:]
		self.intvs = list(range(len(self.dtrue)))
		self.spanintvs = []
		for xx in range(len(self.intvs)):
			self.spanintvs += [itvstruct(xx)]

	def runsim(self,ob, load = False):
		if not load:
			self.execmbuy(ob,self.matbuy,[self.intvs[-1]])
			self.execmbuy(ob,self.matbuy,self.intvs[96:])
			handle =open('buysignal.pickle', 'wb') 
			pickle.dump(self.sigbuy, handle, protocol=pickle.HIGHEST_PROTOCOL)
			handle.close()
			handle =open('sellsignal.pickle', 'wb') 	
			self.execmsell(ob,self.matsell,self.intvs[96:])
			pickle.dump(self.sigsell, handle, protocol=pickle.HIGHEST_PROTOCOL)
			handle.close()
		else:
			pray = self.quarter(deepcopy(self.prices['SPY'][1+self.skip*4:]))
			tray = self.quarter(deepcopy(self.prices['TICK-NASD'][1+self.skip*4:]))
			nray = self.quarter(deepcopy(self.prices['TICK-NYSE'][1+self.skip*4:]))
			cor_to_tick= deepcopy(self.matbuy[62])
			#print (len(pray), len(cor_to_tick),len(self.spanintvs))
			#sys.exit()
			#cor_to_tick_sell = deepcopy(self.matsell[62])
			for xx in range(len(self.spanintvs)):
				self.spanintvs[xx].pricetarg = pray[xx]
				self.spanintvs[xx].prtick_nyse = tray[xx]
				self.spanintvs[xx].prtick_nasd = nray[xx]
				self.spanintvs[xx].targ_cor_nysetick = cor_to_tick[xx]
			#print(len(cor_to_tick_buy))
			#print(len(self.dtrue))
			#sys.exit()
			handle = open('buysignal.pickle', 'rb')
			buysigs = pickle.load(handle)
			handle.close()
			handle = open('sellsignal.pickle', 'rb')
			sellsigs = pickle.load(handle)
			buytrigs = []
			selltrigs =[]
			handle.close()
			for ky in buysigs.sigdic.keys():
				for ii, lo in enumerate(buysigs.sigdic[ky]['itvfired']):
					buytrigs += [[ky, self.dtrue[buysigs.sigdic[ky]['itvfired'][ii]], buysigs.sigdic[ky]['itvfired'][ii], 
				   buysigs.sigdic[ky]['prob_neg_one'][ii], buysigs.sigdic[ky]['prob_pos_one'][ii], pray[lo],tray[lo], nray[lo],cor_to_tick[lo]]]
			buytrigs = sorted(buytrigs, key = itemgetter(2))
			for trig in buytrigs:
				self.spanintvs[trig[2]].bpredmods += [trig[0]]
				self.spanintvs[trig[2]].b_prob_neg_ones += [trig[3]]
				self.spanintvs[trig[2]].b_prob_pos_ones += [trig[4]]
			for ky in sellsigs.sigdic.keys():
				for ii, lo in enumerate(sellsigs.sigdic[ky]['itvfired']):
					selltrigs += [[ky, self.dtrue[sellsigs.sigdic[ky]['itvfired'][ii]], sellsigs.sigdic[ky]['itvfired'][ii], 
				   sellsigs.sigdic[ky]['prob_neg_one'][ii], sellsigs.sigdic[ky]['prob_pos_one'][ii], pray[lo],tray[lo], nray[lo],cor_to_tick[lo]]]
			
			selltrigs = sorted(selltrigs, key = itemgetter(2))
			for trig in selltrigs:
				self.spanintvs[trig[2]].spredmods += [trig[0]]
				self.spanintvs[trig[2]].s_prob_neg_ones += [trig[3]]
				self.spanintvs[trig[2]].s_prob_pos_ones += [trig[4]]
			fout = open (ob.pths['lpath']+self.target+self.seelist, 'w')
			for strc in self.spanintvs:
				fout.write(str(strc.pricetarg)+','+str(strc.prtick_nyse)+','+str(strc.prtick_nasd)+','+str(strc.targ_cor_nysetick)+','+str(len(strc.bpredmods)) +','+str(len(strc.spredmods)))
				if strc.b_prob_neg_ones != []:
					fout.write(','+str(mean(strc.b_prob_neg_ones )))
				else: fout.write(',0')
				if strc.b_prob_pos_ones != []:
					fout.write(','+str(mean(strc.b_prob_pos_ones )))
				else: fout.write(',0')
				if strc.s_prob_neg_ones != []:
					fout.write(','+str(mean(strc.s_prob_neg_ones )))
				else: fout.write(',0')
				if strc.s_prob_pos_ones != []:
					fout.write(','+str(mean(strc.s_prob_pos_ones ))+'\n')
				else: fout.write(',0\n')
			fout.close()
		"""
		class signal(object):
		def __init__(self, lint):
			self.sigdic = {}
			for xx in range(lint):
				self.sigdic[xx]={}
				self.sigdic[xx]['itvfired'] =[]
				self.sigdic[xx]['dtstamp'] =[]
				self.sigdic[xx]['prob_neg_one'] =[]
				self.sigdic[xx]['prob_pos_one'] =[]

		buytrigs = []
		selltrigs = []
		for ky in self.sigbuy.sigdic.keys():
			if lo in self.sigbuy.sigdic[ky]['itvfired']:
				if self.sigbuy.sigdic[ky]['prob_neg_one'][-1] >= float(ob.calc['sim_prob_filter']):
					buytrigs += [ky]
		for ky in self.sigsell.sigdic.keys():
			if lo in self.sigsell.sigdic[ky]['itvfired']:
				if self.sigsell.sigdic[ky]['prob_neg_one'][-1] >= float(ob.calc['sim_prob_filter']):
					selltrigs += [ky]
		print ('buytrigs', buytrigs)
		print ('selltrigs', selltrigs)
		if len(buytrigs) > len(selltrigs):
			qprice = self.quarter(self.prices[ob.calc['sim_targ']])
			buyp = qprice[lo]
			shares = float(ob.calc['sim_tran_capital'])/ buyp
			self.tranlist += [tran('buy',lo,self.dtrue[lo],buyp,shares,'open', 'long')]
			continue
		if len(selltrigs) > len(buytrigs):
			qprice = self.quarter(self.prices[ob.calc['sim_targ']])
			sellp = qprice[lo]
			shares = float(ob.calc['sim_tran_capital']) / sellp
			self.tranlist += [tran('sell',lo,self.dtrue[lo],sellp,shares,'close', 'long')]
		"""

	def quarter(self, ray):
		ot = []
		for lo in range(3, len(ray), 4):
			ot += [ray[lo]]
		return ot

	def fillraydict(self, ob, ky):# Load the pickled arrays
		path = ob.pths['pickle_dir']+ob.pths['sim_curp']+'/'+ky+'.pickle'
		handle = open(path, 'rb')
		ittp = pickle.load(handle)
		handle.close()
		return ittp
	
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
		if bos == 'buy':
			self.sigbuy = signal(len(lins))
		if bos == 'sell':
			self.sigsell = signal(len(lins))
		for i, li in enumerate(lins):
			lis = li.split(',')
			with open(secroot + lis[16], 'rb') as handle:
				gdic[i] = pickle.load(handle)
			hdic[i] = self.joinlint(lis[17:])
			takdic[i] = int(lis[13])

	def sort_args(self, goin, argorder):
		nugoin = []
		for x in argorder:
			nugoin += [goin[x]]
		return nugoin
	
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
	
	def joinlint(self, li):
		slist = []
		for x in li:
			slist += [int(x)]
		return slist
	
	def column(self, matrix, i):
		return [row[i] for row in matrix]
	
	#self.sigdic[xx]['itvfired'] =[]
	#self.sigdic[xx]['dtstamp'] =[]
	#self.sigdic[xx]['prob_neg_one'] =[]
	#self.sigdic[xx]['prob_pos_one'] =[]
	def execmbuy(self, ob, mat, spot):
		for mimf in spot:
			print (mimf)
			self.goinraw = deepcopy(self.column(mat,mimf)[:ob.last_calc_int+1])
			self.goin = self.joinl(self.goinraw)
			if ob.pths['log_goin_sim'] == 'y':
				self.wr_line(self.goinfilerawbuy, str(self.goinraw))
				# The argument order of the first prediction module, disregarding the
				# tak variable is used as an example. This will likely be the same
				# for all prediction modules.
				self.wr_line(self.goinfilebuy, str(self.sort_args(self.goin, self.menhugsbuy[0])))
				self.wr_line(self.buypreddex, str(self.menhugsbuy[0]))
				self.wr_line(self.goinargrawbuy, str(list(range(len(self.goinraw)))))
			sum_men = 0
			if ob.calc['write_adaboost_sim'] == 'y':
				fout = open(self.adafilemenb, 'a')
			for   cou, ky in enumerate(list(self.menbuy.keys())):
				# Put the input data in the list goin into
				# the correct sequence
				nugoin = self.sort_args(self.goin, self.menhugsbuy[ky])
				if ob.pths['log_goin_sim'] == 'y':
					self.wr_line(self.goinargbuy, str(nugoin))
					self.wr_line(self.goinargdexbuy, str(self.menhugsbuy[ky]))
				xray = rayy(nugoin[-1 * self.mentakbuy[ky]:])
				if ob.pths['log_goin_sim'] == 'y':
					self.wr_line(self.xraydexbuy, str(self.menhugsbuy[ky][-1 * self.mentakbuy[ky]:]))
					self.wr_line(self.xrayfloatbuy, str(list(xray)))
				xray = xray.reshape(1, -1)  # if it contains a single sample.
				val = self.menbuy[ky].predict(xray)[0]
				if val == -1:
					self.sigbuy.sigdic[cou]['itvfired'] += [mimf]
				prob = self.menbuy[ky].predict_proba(xray)[0]
				if val == -1:
					self.sigbuy.sigdic[cou]['prob_neg_one'] += [prob[0]]
					self.sigbuy.sigdic[cou]['prob_pos_one'] += [prob[1]]
				if ob.calc['write_adaboost_sim'] == 'y':
					if val == -1 and prob[0] >= self.prob_filter:
						fout.write(str(cou) + ',')
				if val == -1:
					sum_men += 1
			if ob.calc['write_adaboost_sim'] == 'y':
				fout.write(str(sum_men)+'\n')
				fout.close()

	def execmsell(self, ob, mat, spot):
		for mimf in spot:
			print(mimf)
			self.goinraw = deepcopy(self.column(mat,mimf)[:ob.last_calc_int+1])
			self.goin = self.joinl(self.goinraw)
			if ob.pths['log_goin_sim'] == 'y':
				self.wr_line(self.goinfilerawsell, str(self.goinraw))
				# The argument order of the first prediction module, disregarding the
				# tak variable is used as an example. This will likely be the same
				# for all prediction modules.
				self.wr_line(self.goinfilesell, str(self.sort_args(self.goin, self.menhugssell[0])))
				self.wr_line(self.sellpreddex, str(self.menhugssell[0]))				
				self.wr_line(self.goinargrawsell, str(list(range(len(self.goinraw)))))
			sum_men = 0
			if ob.calc['write_adaboost_sim'] == 'y':
				fout = open(self.adafilemens, 'a')
			for cou, ky in enumerate(list(self.mensell.keys())):
				# Put the input data in the list goin into
				# the correct sequence.
				nugoin = self.sort_args(self.goin, self.menhugssell[ky])
				if ob.pths['log_goin_sim'] == 'y':
					self.wr_line(self.goinargsell, str(nugoin))
					self.wr_line(self.goinargdexsell, str(self.menhugssell[ky]))
				xray = rayy(nugoin[-1 * self.mentaksell[ky]:])
				if ob.pths['log_goin_sim'] == 'y':
					self.wr_line(self.xraydexsell, str(self.menhugssell[ky][-1 * self.mentaksell[ky]:]))
					self.wr_line(self.xrayfloatsell, str(list(xray)))
				xray = xray.reshape(1, -1)  # if it contains a single sample.
				val = self.mensell[ky].predict(xray)[0]
				if val == -1:
					self.sigsell.sigdic[cou]['itvfired'] += [mimf]
				prob = self.mensell[ky].predict_proba(xray)[0]
				if val == -1:
					self.sigsell.sigdic[cou]['prob_neg_one'] += [prob[0]]
					self.sigsell.sigdic[cou]['prob_pos_one'] += [prob[1]]
				if ob.calc['write_adaboost_sim'] == 'y':
					if val == -1 and prob[0] >= self.prob_filter:
						fout.write(str(cou) + ',')
				if val == -1:
					sum_men += 1
			if ob.calc['write_adaboost_sim'] == 'y':
				fout.write(str(sum_men)+'\n')
				fout.close()

	def wr_line(self, fi, linee):
		linee = linee.replace('[','')
		linee = linee.replace(']','')
		fout = open(fi, 'a')
		fout.write(linee+'\n')
		fout.close()
obb=figsim.par()
obb.add_list('conflate',obb.tre['conflate_fullx'])
ob = nov_admin.symb(obb,False,False,False)
obx = struct_calc.calk(ob, False)
simob = simu(obx.cob)
simob.runsim(obx.cob, True)
#print (obx.rdi['train']['dates'])
    