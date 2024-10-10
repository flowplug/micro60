import os
from numpy import zeros
from copy import deepcopy
import datetime as dtt
import brownian
import secdb
import interv
import pickle
from statistics import mode
import sys

class fills (object):
	def __init__(self):
		self.wwdb =  secdb.dbp()
		self.inter = interv.interpolate()
		self.interval_int = 60 #int(ob.cob.calc['intervall'])
		self.wwdb =  secdb.dbp()

	def dict_init(self,ob):
		if ob.cob.pths['log_candles'] == 'y':
			isExist =os.path.exists(ob.cob.pths['candle_dir'])
			if not isExist:
				os.makedirs(ob.cob.pths['candle_dir'])
			fout = open(ob.cob.pths['candle_dir']+'/candles.txt','w')
			fout.close()	
		self.dtrue = ob.cob.rdi['live']['dtrue']
		self.len_fields = len(ob.cob.fields)
		self.max_of_mins = 0
		self.covered={}
		self.loy= {}
		self.b4loy={}
		self.ply_dic= {}
		self.covered_dic = {}
		self.nucovered_dic = {}
		self.dup_dic={}
		self.missing_dic ={}
		self.first={}
		# sy is the integer index of the ticker symbols.
		for sy, dummy in enumerate(ob.cob.avg_symbs):
			self.first[sy] = True
			self.covered[sy] = []
			self.loy[sy] = 0
			self.b4loy[sy] = 0
			self.ply_dic[sy] = []
			self.dup_dic[sy] = []
			self.missing_dic[sy] = []
			self.covered_dic[sy] = []
			self.nucovered_dic[sy] = []
			
	def log_candles(self, dex, sy, rays, ob, fille):
		for lo in self.covered[dex]:
			fout = open(fille, 'a')
			outmat = zeros((self.len_fields))
			qlo = lo * self.len_fields
			ou = -1
			for _ in ob.cob.fields:
				ou += 1
				outmat[ou] = deepcopy(rays[0][ob.cob.vlo[sy + 'flat']][qlo+ou])
			fout.write(sy + '  ' + self.dtrue[lo] + ': ')
			for y in range(self.len_fields):
				if y != self.len_fields -1:
					fout.write(str(outmat[y]) + '\t')
				else:
					fout.write(str(outmat[y]) + '\n')
			fout.close()

	def sync_rays(self, rays, ob, init_prior_prices):
		# find mode of the maximum covered interval location integers.
		maxes = []
		for ky in self.covered.keys():
			maxes += [max(self.covered[ky])]
		mode_maxes = mode (maxes)
		print ('mode ',mode_maxes)
		for ky in self.covered.keys():
			maxli =max(self.covered[ky])
			if  maxli < mode_maxes:
				self.fill_missing_sync( list(range(maxli,mode_maxes+1)), ob, rays, ky)
		if init_prior_prices:
			mins = []
			for ky in self.covered.keys():
				mins += [min(self.covered[ky])]
			self.max_of_mins = max(mins)
			if ob.cob.calc['prior_pickle'] == 'y':
				self.load_prior_prices(rays,ob,self.max_of_mins)
			if ob.cob.calc['brownian_bridge'] == 'y':
				self.load_bridges(rays,ob,self.max_of_mins)
			if ob.cob.pths['write_prepend'] == 'y':
				self.log_mats(ob,rays,self.max_of_mins-int(ob.cob.calc['window']), self.max_of_mins)
		# Set the timing array at the modal value.
		for xx in range(self.max_of_mins, mode_maxes+1):
			rays[0][-1][xx] = 1  # The last shared array is 'timing'
		self.max_of_mins = mode_maxes

	def fill_missing_sync(self, missing, ob, rays, sy):
		ticker = ob.cob.avg_symbs[sy]
		print (ticker, str(missing))
		#for lo in missing:
		loo = missing[0] - 1
		end_gap = missing[-1]+1
		#loo, end_gap = self.closest_prior(lo, self.covered[sy])
		quadloo = self.len_fields * loo
		# Get closing value for the closest prior interval.
		val = rays[0][ob.cob.vlo[ticker + 'flat']][quadloo + 3]
		self.fill_empties(ob, rays, ticker, val, loo + 1, end_gap)

	def closest_prior(self, lo, cov):
		ou = -1
		for xx in cov:
			ou += 1
			if xx - 1 >= lo:
				low_near = cov[ou - 1]
				end_gap = cov[ou]
				break
		return low_near, end_gap

	def call_fmiss(self, lst):
		return [x for x in range(lst[0], lst[-1] + 1) if x not in lst]

	def fill_missing(self,missing,ob,rays,sy):
		ticker = ob.cob.avg_symbs[sy]
		if self.b4loy[sy] == 0 :
			# If there is no prior data, use
			# the preset prior value to fill in
			# empty intervals.
			val = ob.cob.fills[ob.cob.avg_symbs[sy]]
			for lo in missing:
				loo, end_gap = self.closest_prior(lo,self.covered[sy])
				self.fill_empties(ob, rays, ticker, val, loo+1, end_gap)
		else:
			for lo in missing:
				loo, end_gap = self.closest_prior(lo,self.covered[sy])
				quadloo = len(ob.cob.fields) * loo
				# Get closing value for the closest prior interval.
				val = rays[0][ob.cob.vlo[ticker + 'flat']][quadloo+3]
				self.fill_empties(ob,rays,ticker,val, loo+1, end_gap)

	def fill_empties(self, ob, rays, sy, val, loo, end_gap):
		for yy in range(loo,end_gap ):
			quadyy = self.len_fields * yy
			for i,fie in enumerate(ob.cob.fields):
				rays[0][ob.cob.vlo[sy + 'flat']][quadyy+i] = val

	def find_hloc(self, val,lo,rays,ob,syy):
		sy = ob.cob.avg_symbs[syy] # Get text ticker to locate the
		# correct shared array.
		quadlo = len(ob.cob.fields) * lo
		if self.first[syy]:
			# If it is the first entry in this interval for the
			# ticker, fill open, high,low, close with the same value val.
			for i,fie in enumerate(ob.cob.fields):
				rays[0][ob.cob.vlo[sy + 'flat']][quadlo+i] = val
			self.first[syy] = False
			return
		if rays[0][ob.cob.vlo[sy + 'flat']][quadlo] == 0.0:
				rays[0][ob.cob.vlo[sy + 'flat']][quadlo] = val
		rays[0][ob.cob.vlo[sy + 'flat']][quadlo+3] = val #closing value
		if rays[0][ob.cob.vlo[sy + 'flat']][quadlo+2] == 0.0:
			rays[0][ob.cob.vlo[sy + 'flat']][quadlo+2] = val
		if rays[0][ob.cob.vlo[sy + 'flat']][quadlo+1] == 0.0:
			rays[0][ob.cob.vlo[sy + 'flat']][quadlo+1] = val
		# The above few lines might not be necessary, but this works.
		# I don't want to test without it.
		if val < rays[0][ob.cob.vlo[sy + 'flat']][quadlo+2]:
			rays[0][ob.cob.vlo[sy + 'flat']][quadlo+2] = val
		if val > rays[0][ob.cob.vlo[sy + 'flat']][quadlo+1]:
			rays[0][ob.cob.vlo[sy + 'flat']][quadlo+1] = val

	def ohlc(self,nuply,ob,rays,sy):
		self.first[sy] = True
		self.popped=[]
		for pz in nuply:
			if pz[3]  in self.dup_dic[sy]:
				lodup = self.dup_dic[sy].index(pz[3])
				self.popped +=[self.dup_dic[sy].pop(lodup)]
				self.first[sy] = False
				self.find_hloc(pz[2], pz[3],rays,ob,sy)
			if pz[3] in self.popped:
				self.first[sy] = False
			self.find_hloc(pz[2], pz[3], rays, ob, sy)

	def qdeal(self, ob,  rays):
		self.dict_init(ob)
		dummy, cur = self.wwdb.conn15('xax')
		timeb4 = dtt.datetime.now()
		b4interval = self.inter.locate_interval(self.dtrue, self.interval_int, timeb4)
		initialize_prior_prices = True
		while 1:
			broken = False
			nuply = self.wwdb.fetchd(str(timeb4), cur)
			if not nuply:
				continue
			current_interval = self.inter.locate_interval(self.dtrue, self.interval_int, list(nuply[-1])[0])
			if current_interval == b4interval: continue
			b4interval = current_interval
			for re in nuply:
				#if re[2] != int(ob.cob.acceptable_types):
					#continue
				re = list(re) # This call to list() is maybe needed because Postgres returns tuples. 
				re += [self.inter.locate_interval(self.dtrue, self.interval_int, re[0])]
				# The function self.inter.locate_interval(self.dtrue, self.interval_int, re[0]) 
				# returns the integer that locates the interval in the timestap array self.dtrue.
				re = re[1:] # Drop the datetime object in the first field, we have located
				# the integer interval in self.dtrue and placed it at the end of record re.
				# Therefore we no longer need the timestamp at re[0].
				# The first field in the record is now the integer locating the ticker in
				# the symbol list at ob.cob.avg_symbs.
				self.ply_dic[re[0]] += [ re ]			
			if ob.cob.calc['mark_data_cycles'] == 'y':
				timeb4 = dtt.datetime.now()	
				print (timeb4)
			for sy, dummy in enumerate(self.ply_dic.keys()):
				if not broken:
					if len(self.ply_dic[sy]) < 1:
						broken = True
				else: break
			if broken:
				continue
			for sy in self.ply_dic.keys():
				if self.ply_dic[sy][-1][3] in self.covered[sy]:
					# If the interval was already covered in a prior interation,
					# place the interval number in self.dup_dic
					self.dup_dic[sy] += [self.covered[sy][-1]]
				for it in self.ply_dic[sy]:
						self.covered[sy] +=[it[3]] # Only the interval number into covered.
				missing = self.call_fmiss(self.covered[sy]) # If there are missing intervals
				# place them in the list 'missing'.
				self.nucovered_dic[sy] = sorted(list(set(missing+self.covered[sy])))
				self.b4loy[sy] = self.loy[sy]
				self.loy[sy] = self.nucovered_dic[sy][-1]
				self.missing_dic[sy] += missing
				self.ohlc(self.ply_dic[sy], ob, rays, sy)
				if self.missing_dic != []:
					self.fill_missing(self.missing_dic[sy], ob, rays, sy)
				self.covered[sy] = sorted(
					list(set(self.covered_dic[sy] + self.covered[sy] + self.nucovered_dic[sy])))
				#if self.missing_dic != []:
					#self.fill_missing(self.missing_dic[sy], ob, rays, sy)
				self.covered_dic[sy] = []
				self.missing_dic[sy] = []
				self.dup_dic[sy] = []
				self.first[sy] = True
			self.sync_rays(rays, ob, initialize_prior_prices)
			initialize_prior_prices = False
			if ob.cob.pths['log_candles'] == 'y':
				for lo, sy in enumerate(ob.cob.avg_symbs):
					filee = ob.cob.calc['candle_dir']+'/candles.txt'
					fout = open(filee, 'a')
					fout.write('\n' + sy + ': \n')
					fout.close()
					self.log_candles(lo, sy, rays, ob, filee)

	def load_bridges(self, rays,ob, max_mins):
		rang = list(range((max_mins-int(ob.cob.calc['window']))*self.len_fields,(max_mins*self.len_fields)))
		for ticker in ob.cob.avg_symbs:
			if ticker == 'TICK-NYSE':
				list_bridge = []
				for ctt in ob.cob.tick_nyse:
					list_bridge  += [float(ctt)]
				for i,lo in enumerate(rang):
					rays[0][ob.cob.vlo[ticker + 'flat']][lo+1] = list_bridge[i]
				continue
			if ticker == 'TICK-NASD':
				list_bridge = []
				for ctt in ob.cob.tick_nasd:
					list_bridge  += [float(ctt)]
				for i,lo in enumerate(rang):
					rays[0][ob.cob.vlo[ticker + 'flat']][lo+1] = list_bridge[i]
				continue
			list_bridge = self.get_brown(rays[0][ob.cob.vlo[ticker + 'flat']][max_mins*self.len_fields], len(rang))
			for i,lo in enumerate(rang):
				rays[0][ob.cob.vlo[ticker + 'flat']][lo+1] = list_bridge[i]
		rays[0][-1][0] = max_mins-int(ob.cob.calc['window'])

	def get_brown(self,val,lenn):
		lista = brownian.brown(lenn,1,.05,val, val)
		ohlc_list = []
		ou = -1
		for vx in lista:
			ou += 1
			if ou == 0:
				inlist = []
			inlist += [vx]
			if ou == 3:
				max_inlist = max(inlist)
				min_inlist = min(inlist)
				inlist[1] = max_inlist
				inlist[2] = min_inlist
				ohlc_list += inlist
				ou = -1
		return ohlc_list
	
	def load_prior_prices(self, rays,ob, max_mins):
		ray_dict= {}
		path = ob.calc['pickle_dir']+'/'+ob.pths['curp']
		fi = path+'/train.pickle'
		with open(fi, 'rb') as handle:
			ray_dict[ky] = pickle.load(handle)
		rang = list(range((max_mins-int(ob.cob.calc['window']))*self.len_fields,(max_mins*self.len_fields)+1))
		rang.reverse()
		for ticker in ob.cob.avg_symbs:
			bak_lo = -1
			for lo in rang:
				rays[0][ob.cob.vlo[ticker + 'flat']][lo] = ray_dict[ky][ticker][bak_lo]
				bak_lo -= 1
		rays[0][-1][0] = max_mins-int(ob.cob.calc['window'])
		
	def log_mats(self,ob,rays,bgg,endd):
		# if ob.cob.pths['write_prepend'] == 'y':

		fout = open(ob.cob.pths['chkpath']+'matchek'+str(endd)+'.csv','w')
		for sy in ob.cob.avg_symbs:
			fout.write(sy+',')
			for xx in range(bgg*self.len_fields,(self.len_fields*endd)+1):
					if xx != endd*4:
						fout.write(str(rays[0][ob.cob.vlo[sy + 'flat']][xx])+',')
					else:
						fout.write(str(rays[0][ob.cob.vlo[sy + 'flat']][xx])+'\n')
		fout.close()
		


if __name__ == "__main__":					
	read_ob = fills()
	lis = read_ob.get_brown(50,380)
	print (lis)
	print (len(lis))
	sys.exit()
	read_ob.load_prior_prices([ob.cob.argtuple],ob, 720 )
	read_ob.log_mats(ob,[ob.cob.argtuple],625,720)
