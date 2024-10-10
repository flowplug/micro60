import dates
from copy import deepcopy
import datetime
import time
import sys
class dafil(object):
	def __init__(self):
		pass

	def udateg(self, trueray):
		uniquedates = dates.dayx(deepcopy(trueray))
		return dates.dayxb(deepcopy(trueray),uniquedates)

	def rundi(self,ob, rdi):
		if ob.calc['live'] == 'y':
			Y,M,D,H,m,ss,g,h,i=time.localtime()
			b = eval(ob.calc['begtall']) # usually begtall = (0,0,0)
			e = eval(ob.calc['endall']) # endall = (23,59,45)
			sta= str(datetime.datetime(Y,M,D,b[0],b[1],b[2]))
			endd=str(datetime.datetime(Y,M,D,e[0],e[1],e[2]))
			rdi['live']['dtrue'] = dates.gettruesecmb (sta,endd, int(ob.calc['intervall']), 'y')
			rdi['live']['dates'] = self.udateg(rdi['live']['dtrue'])
		else:
			if ob.calc['intervall'] == '60':
				if ob.calc['validate'] == 'y':
					st = ob.calc['beginvalidation'].split(' ')
					sta = str(datetime.datetime(int(st[0]),int(st[1]),int(st[2]),int(st[3]),int(st[4]),int(st[5])) )
					st =ob.calc['endvalidation'].split(' ')
					endd =str( datetime.datetime(int(st[0]),int(st[1]),int(st[2]),int(st[3]),int(st[4]),int(st[5])) )
					rdi['valid']['dtrue'] = deepcopy(dates.gettruesecmb (sta,endd, int(ob.calc['intervall']), 'n' ))
					rdi['valid']['dates'] = self.udateg(rdi['valid']['dtrue'] )
				if ob.calc['train'] == 'y':
					st = ob.calc['begintrain'].split(' ')
					sta = str(datetime.datetime(int(st[0]),int(st[1]),int(st[2]),int(st[3]),int(st[4]),int(st[5])) )
					st =  ob.calc['endtrain'].split(' ')
					endd =str( datetime.datetime(int(st[0]),int(st[1]),int(st[2]),int(st[3]),int(st[4]),int(st[5])) )
					rdi['train']['dtrue'] = deepcopy(dates.gettruesecmb(sta, endd, int(ob.calc['intervall']), 'n'))
					rdi['train']['dates'] = self.udateg(rdi['train']['dtrue'] )
			

	


