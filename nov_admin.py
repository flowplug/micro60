import sys
import os
import dayfill
import secdb
from multiprocessing import Array # Array is used withina string executed with exec()

class symb(object):
	def __init__(self,ob ,init_db_table=False, read_fill_file = True, load_shared_arrays = True):
		if init_db_table:
			db = secdb.dbp()
			db.crtable15('xax', True)
		self.calc ={}
		self.tre = {}
		self.pths={}
		self.conflate = ob.conflate
		for ky in ob.calc.keys():
			self.calc[ky] = ob.calc[ky]
		for ky in ob.pths.keys():
			self.pths[ky] = ob.pths[ky]
		for ky in ob.tre.keys():
			self.tre[ky] = ob.tre[ky]
		self.acceptable_types = []
		self.acceptable_types = int(ob.calc['acceptable_tick_type'])
		self.avg_symbs=[]
		self.fields = self.calc['std_fields'].split(',')
		self.contracts = self.gen_kons(ob) # Also fills self.avg_symbs
		self.fills = {}
		if read_fill_file:
			for rec in ob.conflate_fill:
				rec = rec.split(',')
				sy = rec[0]
				self.fills[sy] = float(rec[1])
		self.rdi = self.ddate(ob)
		if load_shared_arrays:
			if ob.calc['live'] == 'y':
				self.vlo = {}
				self.get_avg_vars('flat')
				self.argtuple = self.shared_arrays(len(ob.rdi['live']['dates']), int(ob.calc['array_len']))

	def gen_kons(self,ob):
		dows =[]
		for lin in ob.conflate:
			d={}
			linlist= lin.split(',')
			syy = linlist[0].strip()
			if '\n' in list(syy): syy = syy.replace('\n','')
			self.avg_symbs+=[syy]
			if (len(linlist) == 1):
				tic = linlist[0].strip()
				d['symbol']=tic
				d['exchange']=self.calc['default_exchange']
				d['secType'] = self.calc['default_security_type']
				d['currency'] = self.calc['default_currency']
			if (len(linlist) == 2):
				tic = linlist[0].strip()
				d['symbol'] = tic
				d['exchange'] = linlist[1].strip()
				d['secType'] = self.calc['default_security_type']
				d['currency'] = self.calc['default_currency']
			if (len(linlist) == 3):
				tic = linlist[0].strip()
				d['symbol'] = tic
				d['exchange'] = linlist[1].strip()
				d['currency'] = self.calc['default_currency']
				chk = linlist[2].find('\n')
				if chk == -1:
					d['secType'] = linlist[2].strip()
				else:
					d['secType'] = linlist[2][:-1].strip()
			if (len(linlist) == 4):
				tic = linlist[0].strip()
				d['symbol'] = tic
				d['exchange'] = linlist[1].strip()
				d['secType'] = linlist[2].strip()
				d['currency'] = self.calc['default_currency']
				chk = linlist[3].find('\n')
				if chk == -1:
					d['expiry'] = linlist[3].strip()
				else:
					d['expiry'] = linlist[3][:-1].strip()
			dows += [d]
		return dows

	def ddate(self,ob):
		ob.rdi = {}
		ob.rdi['valid'] = {}
		ob.rdi['train'] = {}
		ob.rdi['live'] = {}
		dob = dayfill.dafil()
		dob.rundi(ob,ob.rdi)
		return ob.rdi

	def shared_arrays(self, day_count, raylen):
		field_count =  len(self.fields)
		lll = raylen * day_count
		#print (day_count)
		flat_array_len = field_count* lll * day_count
		for yg in range(int(self.nvars)):
			exec('a' + str(yg) + "= Array('d',flat_array_len *[0.0])")
		argl = '['
		for ij in range(int(self.nvars)):
			argl += 'a' + str(ij) + ','
		lisarg = list(argl)
		argl.join(lisarg)
		argl += ']'
		argl = argl.replace(",]", "]")
		argtuple = eval(argl)
		return argtuple

	def get_avg_vars( self, slug ):
		cou= -1
		for zz in self.avg_symbs+['timing']:
				cou += 1
				self.vlo[zz + slug] = cou
		self.nvars = cou + 1



