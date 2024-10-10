#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import configparser
#import secdb


class par(object):
	def __init__(self):
		confi = configparser.ConfigParser()
		location_ini_file = '../config.ini'
		confi.read(location_ini_file)
		self.dirs = confi['DIRS']
		self.dbb= confi['DBB']
		self.pths = confi['PTHS']
		self.tre= confi['TRE']
		self.twr = confi['TWR']
		self.calc = confi['CALC']

	def techs_ini(self):
		confi = configparser.ConfigParser()
		location_ini_file = self.tre['techs']
		confi.read(location_ini_file)
		self.techsl = confi['TECHS']
	def clean_syms(self, list_of_strings ):
		nu_list= []
		for hy in list_of_strings:
			ins =hy.replace('\n','')
			ins=ins.replace('\t','')
			ins=ins.replace(' ','')
			ins=ins.replace('\r','')
			nu_list += [ins]
		return nu_list
	def add_list(self,list_name, file ):
		fin =  open(file)
		listin = self.clean_syms(fin.readlines())
		exec('self.' + list_name + '=listin')


if __name__ == '__main__':
	a = par ()
	for ky in a.dirs.keys():
		if os.path.exists(a.dirs[ky]):
			print('Directory '+a.dirs[ky]+' exists, it will not be created.')
		else:
			print('Directory ' + a.dirs[ky] + ' does not exist, it will be created.')
			os.makedirs(a.dirs[ky])
	b = secdb.dbp()
	b.makedb(a.dbb['dbhost'], a.dbb['parm_dbname'], a.dbb['dbuser'], a.dbb['dbpasswd'])
	b.crtable_new(a.dbb['dbhost'], a.dbb['parm_dbname'], a.dbb['dbuser'],
				  a.dbb['dbpasswd'], 1, a.dbb['parmt0'], a.dbb['parmt0_fields_types'])
	b.writerecs_new(a.dbb['dbhost'], a.dbb['parm_dbname'], a.dbb['dbuser'], a.dbb['dbpasswd'],
					a.calc, a.dbb['parmt0'],a.dbb['parmt0_fields'])
