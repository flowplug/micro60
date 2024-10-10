import datetime as dt

class interpolate(object):
	def locate_interval(self, dtrue, interv, dtob):
		cursec = dtob.second
		if interv == 1:
			sec_slot = cursec
		if interv == 5:
			sec_slot = self.sec5(cursec)
		if interv == 10:
			sec_slot = self.sec10(cursec)
		if interv == 15:
			sec_slot = self.sec15(cursec)
		if interv == 30:
			sec_slot = self.sec30(cursec)
		if interv == 60:
			sec_slot = 0
		dslot = str(dt.datetime(dtob.year, dtob.month, dtob.day, dtob.hour, dtob.minute, sec_slot))
		return dtrue.index(str(dslot))

	def sec5(self,ss):
		if ss >= 0 and ss <5: return 0
		if ss >= 5 and ss <10: return 5
		if ss >= 10 and ss <15: return 10
		if ss >= 15 and ss <20: return 15
		if ss >= 20 and ss <25: return 20
		if ss >= 25 and ss <30: return 25
		if ss >= 30 and ss <35: return 30
		if ss >= 35 and ss <40: return 35
		if ss >= 40 and ss <45: return 40
		if ss >= 45 and ss <50: return 45
		if ss >= 50 and ss <55: return 50
		if ss >= 55 and ss <60: return 55
		if ss ==60 : return 0

	def sec10(self,ss):
		if ss >= 0 and ss <10: return 0
		if ss >= 10 and ss <20: return 10
		if ss >= 20 and ss <30: return 20
		if ss >= 30 and ss <40: return 30
		if ss >= 40 and ss <50: return 40
		if ss >= 50 and ss <60: return 50
		if ss ==60 : return 0

	def sec15(self, ss):
		if ss >= 0 and ss < 15: return 0
		if ss >= 15 and ss < 30: return 15
		if ss >= 30 and ss < 45: return 30
		if ss >= 45 and ss < 60: return 45
		if ss == 60: return 0

	def sec30(self, ss):
		if ss >= 0 and ss < 30: return 0
		if ss >= 30 and ss < 60: return 30
		if ss == 60: return 0
