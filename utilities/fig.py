#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import configparser

class par(object):
	def __init__(self):
		confi = configparser.ConfigParser()
		location_ini_file = '/home/alan2/dev/resources/parameters/config.ini'
		confi.read(location_ini_file)
		self.pths = confi['PTHS']
		self.tre = confi['TRE']
		self.calc = confi['CALC']

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
		