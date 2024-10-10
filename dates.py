# -*- coding: utf-8 -*-
import time
import datetime
import sys
holidays = [(1,1,2008),(1,21,2008), (2,18,2008), (3,21,2008), (5,26,2008),  (7,4,2008), (9,1,2008),
			(11,27,2008), (12,25,2008),(1,1,2009),(1,19,2009),(2,16,2009),(4,10,2009),(5,25,2009),(7,3,2009),(9,7,2009),
			(11,26,2009),(12,25,2009),(1,1,2010),(1,18,2010),(2,15,2010),(4,2,2010),(5,31,2010),(7,5,2010),(9,6,2010),(12,24,2010),
			(9,5,2011),(9,29,2011),(9,30,2011),(10,31,2011),(11,1,2011),(9,8,2011),(12,7,2011) ,(4,23,2012),(5,4,2012),(12,10,2012),
			(1,1,2013),(1,21,2013),(3,29,2013),(4,1,2013),(5,6,2013),(4,15,2022),(3,29,2024),(5,27,2024),(6,19,2024),(7,3,2024),(7,4,2024),(9,2,2024)]
endearly = [ ]
hourmax = 16


dopenh = 9
dopenm = 30	
dcloseh = 15
dclosem = 59
dcloses = 45

def earlyend(date ):
	for x in endearly:
		if (date.month ==x[0]) & (date.day == x[1]) & (date.year == x[2]) & (date.hour >= hourmax): return 1
	return 0

def holiday(date):
	for x in holidays:
		if (date.month ==x[0]) & (date.day == x[1]) & (date.year == x[2]): return 1
	return 0

def notregtimexx(date,idiff):
	if (date.hour < dopenh): return 1
	if (date.hour == dopenh) & (date.minute < dopenm): return 1
	if date.hour > dcloseh:return 1
	return 0

def gettruesecmb (starttrain, endtrain, interval, allh ):
	begin = datetime.datetime(*time.strptime(starttrain, "%Y-%m-%d %H:%M:%S")[0:6])
	end = datetime.datetime(*time.strptime(endtrain, "%Y-%m-%d %H:%M:%S")[0:6])
	trueray = []
	intervaldiff =datetime.timedelta(seconds=interval)
	next = begin #+ intervaldiff
	while next <= end:
		if allh != 'y':
			if (notregtimexx(next,intervaldiff)==1):
				next=next +intervaldiff
				continue
			if (( next.strftime("%A") =='Saturday') | (next.strftime("%A") =='Sunday')):
				next=next +intervaldiff
				continue
			if (holiday(next)==1):
				next=next +intervaldiff
				continue
			if (earlyend(next)==1): # See if it is one of the days when trading ends early.
				next=next +intervaldiff
				continue
		mysqlform = next.strftime("%Y-%m-%d %H:%M:%S")
		trueray += [mysqlform] # If the value 'next' meets the criteria, append.
		next=next +intervaldiff
	return trueray

def dayx (trueray):
		dateray=[]
		count = 0
		for x in trueray:
			b = datetime.datetime(*time.strptime(x, "%Y-%m-%d %H:%M:%S")[0:6])
			y=int (b.strftime("%Y"))
			m=int (b.strftime("%m"))
			d=int (b.strftime("%d"))
			endday = datetime.datetime(y, m, d,23,59,59)
			dateray +=[endday]
			count +=1	
		dateray = list(set(dateray))
		dateray.sort()
		return dateray
	
def dayxb (trueray, ud): # Return the begin minute and end minute of each
			 # trading day in a list
		dr=[]
		f  = trueray[0]
		b4 = trueray[0]
		end = trueray[len(trueray)-1]
		for y in ud:
			while 1:
				if trueray == []:
					break
				if trueray[0] > str(y) or trueray[0] == end:
					e = b4
					if trueray[0] == end: e=end
					dr += [[f,e]]
					f = trueray[0]
					trueray.pop(0)
					if trueray != []:b4 =trueray[0]
					break
				else:
					b4 = trueray[0]
					trueray.pop(0)
		return dr


