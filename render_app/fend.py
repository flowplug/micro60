#!/usr/bin/python 
# -*- coding: utf-8 -*-
import os
def fil(ob):
	ob.fq=ob.proot+'/'+ob.quant_dir
	try:os.makedirs(ob.fq)
	except:pass
	if ob.record_quants=='y' and ob.erase_quants=='y':
		foutb = open ( ob.fq+'/lowq.txt','w')
		foute = open ( ob.fq+'/hiq.txt','w')
		foutf = open ( ob.fq+'/hiqu.txt','w')
		foutbd = open ( ob.fq+'/dlowq.txt','w')
		fouted = open ( ob.fq+'/dhiq.txt','w')
		foutfd = open ( ob.fq+'/dhiqu.txt','w')
		foutbf = open ( ob.fq+'/flowq.txt','w')
		foutef = open ( ob.fq+'/fhiq.txt','w')
		foutff = open ( ob.fq+'/fhiqu.txt','w')

class dtn_fields(object):
   def sfi(self,ob):
        ob.last=int(ob.last)-1
        ob.cumvol=int(ob.cumvol)-1
        ob.curvol=int(ob.curvol)-1
        ob.bid=int(ob.bid)-1
        ob.ask=int(ob.ask)-1
        ob.bids=int(ob.bids)-1
        ob.asks=int(ob.asks)-1
        ob.tick=int(ob.tick)-1
        ob.timef=int(ob.timef)-1 # A character field.
        ob.openint=int(ob.openint)-1
        ob.spread=int(ob.spread)-1
        ob.avgvol=int(ob.avgvol)-1
        ob.bidchange=int(ob.bidchange)-1
        ob.askchange=int(ob.askchange)-1
        ob.vola=int(ob.vola)-1
        ob.daysto=int(ob.daysto)-1
        ob.prevdv=int(ob.prevdv)-1
        ob.vwap=int(ob.vwap)-1
        ob.numeric_fields=[\
        ob.cumvol,\
        ob.curvol,\
        ob.tick,\
        ob.openint,\
        ob.daysto]
        ob.float_fields=[\
        ob.last,\
        ob.bid,\
        ob.ask,\
        ob.bids,\
        ob.asks,\
        ob.spread,\
        ob.avgvol,\
        ob.bidchange,\
        ob.askchange,\
        ob.vola,\
        ob.prevdv,\
        ob.vwap]

class fields(object):
  xlast=0
  xcumvol=1
  xcurvol=2
  xbid=3
  xask=4
  xbids=5
  xasks=6
  xbidsum=7
  xasksum=8
  xopenint=9
  xspread=10
  xavgvol=11
  xbidchange=12
  xaskchange=13
  xvola=14
  xprevdv=15
  xvwap=16
  xdaysto=17
  xl=18
  xo=19
  xh=20
  xbidchangesum=21
  xaskchangesum=22
  xspreadsum=23
  xpoints=24
  xavgvold=25
  xbidl=26
  xbido=27
  xbidh=28
  xaskl=29
  xasko=30
  xaskh=31
  xtickup=32
  xtickdown=33
  xtickunch=34
  xtimef=35
  endv=36
  __slots__=['xlast',\
'xcumvol',\
'xcurvol',\
'xbid',\
'xask',\
'xbids',\
'xasks',\
'xbidsum',\
'xasksum',\
'xopenint',\
'xspread',\
'xavgvol',\
'xbidchange',\
'xaskchange',\
'xvola',\
'xprevdv',\
'xvwap',\
'xdaysto',\
'xl',\
'xo',\
'xh',\
'xbidchangesum',\
'xaskchangesum',\
'xspreadsum',\
'xpoints',\
'xavgvold',\
'xbidl',\
'xbido',\
'xbidh',\
'xaskl',\
'xasko',\
'xaskh',\
'xtickup',\
'xtickdown',\
'xtickunch',\
'xtimef',\
'endv']

  def sfx(self,ob):
    ob.xlast=0
    ob.xcumvol=1
    ob.xcurvol=2
    ob.xbid=3
    ob.xask=4
    ob.xbids=5
    ob.xasks=6
    ob.xbidsum=7
    ob.xasksum=8
    ob.xopenint=9
    ob.xspread=10
    ob.xavgvol=11
    ob.xbidchange=12
    ob.xaskchange=13
    ob.xvola=14
    ob.xprevdv=15
    ob.xvwap=16
    ob.xdaysto=17
    ob.xl=18
    ob.xo=19
    ob.xh=20
    ob.xbidchangesum=21
    ob.xaskchangesum=22
    ob.xspreadsum=23
    ob.xpoints=24
    ob.xavgvold=25
    ob.xbidl=26
    ob.xbido=27
    ob.xbidh=28
    ob.xaskl=29
    ob.xasko=30
    ob.xaskh=31
    ob.xtickup=32
    ob.xtickdown=33
    ob.xtickunch=34
    ob.xtimef=35
    ob.endv=36
