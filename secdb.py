#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import psycopg2 as psy
class dbp(object):
	def __init__(self):
		pass
	def fetchd(self,st, cur):
		sertstr = "SELECT * FROM points as S WHERE S.time >='%s' ORDER BY S.time" % (st)
		cur.execute(sertstr)
		return cur.fetchall()
	
	def insert_list(self, dbname, list):
		conn = psy.connect(host="localhost", database=dbname, user="alan2", password="Nenvy23!")
		sql = "INSERT INTO points (time, sym, typ, price) VALUES (%s, %s, %s, %s)"
		cursor = conn.cursor()
		cursor.executemany(sql, list)
		conn.commit()
		conn.close()
		cursor.close()

	def conn15(self, dbname):
		conn = psy.connect(host="localhost", database=dbname,user="alan2", password="Nenvy23!")
		cursor = conn.cursor()
		return conn, cursor
	
	def crtable15(self, dbname, drop):
		conn = psy.connect(host="localhost", database=dbname, user="alan2", password="Nenvy23!")
		sql = '''CREATE TABLE points (time timestamp without time zone NOT NULL,sym int, typ int, price float);'''
		if drop: # Without 'cascade' postgres hangs probably because the index isn't automatically dropped
			# without cascade
			sqldrop = '''drop TABLE if exists points cascade;'''
			cursor = conn.cursor()
			cursor.execute(sqldrop)
			conn.commit()
			cursor.close()
			print ('Table dropped if it existed.')
		cursor = conn.cursor()
		cursor.execute(sql)
		conn.commit()
		sql = '''create unique index if not exists pdex on points (time, sym);'''
		cursor.execute(sql)
		conn.commit()
		cursor.close()
		conn.close()
		
	def getdowm(self, fixray, bgp):
		hus = {}
		for x in fixray:
			hus[x] = self.gettrai(x, bgp[0], bgp[1])
		return hus

	def gettrai(self,ticker, st, en ):
		con = psy.connect(host="localhost", database='xax', user="alan2", password="Nenvy23!")
		cur = con.cursor()
		sertstr = "SELECT * FROM candles60 as S WHERE S.Date >='%s' AND S.Date <= '%s' and S.sym = '%s' ORDER BY S.Date" % (st, en, ticker)
		cur.execute(sertstr)
		result = cur.fetchall()
		ret = cur.rowcount
		con.commit()
		cur.close()
		con.close()
		if ret == 0:
			print('No data in database  for table ' + ticker)
			sys.exit()
		return result

