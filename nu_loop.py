from multiprocessing import Process
from ibapi.contract import Contract
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import threading
import time
import secdb
import datetime as dt
import sys
import os
import struct_calc
import strun_live
import physr
import nov_admin
import fig

obb=fig.par()
obb.add_list('conflate',obb.tre['conflate_fullx'])
obb.add_list('fullntargs',obb.tre['fullntargs'])
obb.add_list('conflate_fill',obb.tre['conflate_fillx'])
obb.add_list('tick_nasd', obb.tre['tick_nasd_file'])
obb.add_list('tick_nyse', obb.tre['tick_nyse_file'])
if obb.calc['ib_data_gather'] == 'y':
	obx = nov_admin.symb(obb, True) # The True initiates the points database table.
else:
	obx = nov_admin.symb(obb, False)
ob = struct_calc.calk(obx)
ob.cob.tick_nasd = obb.tick_nasd
ob.cob.tick_nyse = obb.tick_nyse
sym = ob.cob.avg_symbs
tick_type = int(ob.cob.calc['acceptable_tick_type'])
load_size = 64 #128 #increased from 30
db = secdb.dbp()

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
	def tickPrice(self, reqId, tickType, price, attrib):
		if int(tickType) == tick_type:
			self.tak += [[str( dt.datetime.now()), reqId, tickType, price]]
		if len(self.tak) >= load_size:
			self.db.insert_list('xax', self.tak)
			self.tak =[]

def thred( konlist, ob, rays):
	thread1 = threading.Thread(target=pavhh, args=(ob, rays))
	thread1.start()
	if ob.cob.calc['ib_data_gather'] == 'y':
		app = IBapi()
		app.connect('127.0.0.1', 7496, 131313)
		app.db = secdb.dbp()
		app.tak =[]
		def run_loop():
			app.run()
		api_thread = threading.Thread(target=run_loop, daemon=True)
		api_thread.start()
		time.sleep(1)
		for yy, kon in enumerate(konlist):
			app.ply = []
			app.reqMktData(yy, kon, '', False, False, [])
		while 1:
			pass

def avesdow(ob,sec):
	strun_live.alg(ob, sec)

def pavhh(ob,  *d):
	avv = physr.fills()
	avv.qdeal(ob, d)

def main():
	ct = dt.datetime.now()
	daystr = dt.datetime.today().strftime('%Y-%m-%d')
	# Use timestamp of current time to create a unique folder for run information.
	fol = ob.cob.pths['runfolder']+'/'+daystr+'f'+str(ct.timestamp()).replace('.','_')+'/'
	os.makedirs(fol)
	ob.cob.pths['lpath'] = fol
	ob.cob.pths['rpath'] = fol+ob.cob.pths['results_dir'] + '/'
	os.makedirs(ob.cob.pths['rpath'])
	if ob.cob.pths['write_prepend'] == 'y':
		ob.cob.pths['chkpath'] = fol + ob.cob.pths['mat_check_dir'] + '/'
		os.makedirs(ob.cob.pths['chkpath'])
	if ob.cob.pths['log_goin'] == 'y':
		ob.cob.pths['goin'] = fol + ob.cob.pths['log_dir'] + '/'
		os.makedirs(ob.cob.pths['goin'])
	if ob.cob.pths['log_candles'] == 'y':
		ob.cob.pths['candr'] = fol + ob.cob.pths['candle_dir'] + '/'
		os.makedirs(ob.cob.pths['candr'])
	kons = get_kons()
	for sy in obb.fullntargs:
		pcs = [Process(target=avesdow, args=(ob,sy)) for _ in range(1)]
		for p in pcs:
			p.start()
	thred(kons, ob,ob.cob.argtuple )

def get_kons():
	kon_list = []
	for syy in ob.cob.contracts:
		nucon = Contract()
		for ky in syy.keys():
				if ky == 'symbol':
					nucon.symbol = syy[ky]
				if ky == 'secType':
					nucon.secType = syy[ky]
				if ky == 'exchange':
					nucon.exchange = syy[ky]
				if ky == 'currency':
					nucon.currency = syy[ky]
				if ky == 'expiry':
					if nucon.exchange == 'GLOBEX':
						nucon.localSymbol = nucon.symbol+'U2'
					else:
						nucon.lastTradeDateOrContractMonth = syy[ky]
		kon_list += [nucon]
	return kon_list
main()	
