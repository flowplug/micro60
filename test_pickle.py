import sys
import os
import secdb
import nov_admin
from numpy import zeros
import pickle
import glean
import fig
obb=fig.par()
obb.add_list('conflate',obb.tre['conflate_fullx'])
obb.add_list('conflate_fill',obb.tre['conflate_fillx'])
ob = nov_admin.symb(obb)
print (ob.avg_symbs)
dbob = secdb.dbp()

class signal(object):
	def __init__(self, lint):
		self.sigdic = {}
		for xx in range(lint):
			self.sigdic[xx]={}
			self.sigdic[xx]['itvfired'] = []
			self.sigdic[xx]['dtstamp'] = []
			self.sigdic[xx]['prob_neg_one'] = []
			self.sigdic[xx]['prob_pos_one'] = []

#aa =signal(5)
#handle =open('signal.pickle', 'wb') 
#pickle.dump(aa, handle, protocol=pickle.HIGHEST_PROTOCOL)	
"""

# Define a simple structure/class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Create a list of structures
#persons = [
    #Person("Alice", 20),
    #Person("Bob", 30),
    ##Person("Charlie", 25)
#]

# Pickle the list of structures
#with open("persons.pickle", "wb") as file:
    #pickle.dump(persons, file)


# Unpickle the list of structures
with open("persons.pickle", "rb") as file:
    persons = pickle.load(file)

# Print the unpickled list of structures
for person in persons:
    print(person.name, person.age)
"""
handle = open('signal.pickle', 'rb')
aa = pickle.load(handle)
print (aa.sigdic)
#for it in aa:
	#print (it.sigdic[0])
"""
def fillraydict(ob, ky):
	ray = {}
	intervals= len(ob.rdi[ky]['dtrue'])
	fies = len(ob.fields)
	for sy in ob.avg_symbs:
		ray[sy] = zeros((intervals*fies))
	return ray

def main():
	print (ob.pths['curp'])
	raydict={}
	for ky in ob.rdi.keys():
		if ob.rdi[ky] == {}: continue
		raydict[ky] = fillraydict(ob,ky)
	sqldict ={}
	for ky in ob.rdi.keys():
		if ob.rdi[ky] == {}: continue
		span = [ob.rdi[ky]['dtrue'][0], ob.rdi[ky]['dtrue'][-1]]
		print (span)
		print ('length dtrue', len(ob.rdi[ky]['dtrue']) )
		sqldict[ky] = dbob.getdowm(ob.avg_symbs, span)

	# Put SQL recs into arrays
	for ky in ob.rdi.keys():
		if ob.rdi[ky] == {}: continue
		print (ky)
		glean.glee(sqldict[ky], raydict[ky], ob ,ob.rdi[ky]['dtrue']  )
		# Erase the database dictionary
		ob.rdi[ky]['sql_recs'] ={}
		# Pickle the arrays
		path = ob.pths['pickle_dir']+ob.pths['curp']
		isExist =os.path.exists(path)
		if not isExist:
			os.makedirs(path)
		handle =open(path+'/'+ky+'.pickle', 'wb') 
		pickle.dump(raydict[ky], handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
	main()
"""