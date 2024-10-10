from copy import deepcopy
import sys

class loc(object):
	def __init__(self):
		self.tiny = 0.000000000001
		self.chunk = 130

	def find_max_min(self,time_series):
		if not time_series:
			return None, None

		max_value = time_series[0]
		min_value = time_series[0]

		for value in time_series[1:]:
			if value[0] > max_value[0]:
				max_value = value
			elif value[0] < min_value[0]:
				min_value = value

		return [max_value, min_value]

	def link_index(self,ser):
		# ser is a list of floats. For each value create a small
		# list that contains the value in the first position and the 
		# index value in the second position. Because the
		# values in ser might not be unique
		link_ser = []
		ou = 0.0
		for i, val in enumerate(ser):
			ou += self.tiny
			link_ser += [[val+ou,i]]
		return link_ser
	
	def main(self,lis):
		lisf = self.link_index(lis)
		otrak =[]
		b4 = 0
		while 1:
			ranb = deepcopy(lisf[b4:b4+self.chunk])
			otrak += [self.find_max_min(ranb)]
			b4 += self.chunk
			if b4 > len(lisf): 
				break
		buys = len(lisf)* [1]
		sells = len(lisf)*[1]
		for max_min in otrak:
			if max_min[0] != None and max_min[1] != None:
				sells[max_min[0][1]] = -1
				buys[max_min[1][1]] = -1
		return buys,sells
