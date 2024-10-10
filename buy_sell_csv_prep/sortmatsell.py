from operator import itemgetter as itg

menout = 'aamensellNVDA.csv'
arb_large =9999
filter1 = 0
filter2 = .98
filter3 = 3
filter4 =  1.0
filter5 = 0.97
filter6 = 0.06
filter7 = 0.96
filter8 = 0.09
filter9 = .01
def writ(fi,lii):
    fout = open (fi,'w')
    for ku in lii:
        fout.write(ku)

fintx = 'asellNVDA.csv'
fin = open(fintx)
lis = fin.readlines()

print ('rows original matrix:', len(lis))
men = []
for li in lis:
	li=li.replace(',,',',') # Replaces the empty list entry before the column orders fields.
	li = li.replace('../mat_csvs/','')
	lisp = li.split(',')
	if float(lisp[4]) == 1.0 and float(lisp[1]) > 0:
		men += [li]
		continue
	if float(lisp[4])  < filter2:
		continue
	if float(lisp[3]) == filter1: 
		continue
	if float(lisp[3]) < filter9: 
		continue
	#if float(lisp[4])  < filter2:
		#continue
	if (float(lisp[4]) + float(lisp[3]) ) < filter4:
		continue
	#if float(lisp[4]) < filter5 and float(lisp[3])< filter6:
		#continue
	#if float(lisp[4]) < filter7 and float(lisp[3])< filter8:
		#continue
	else:
		men += [li]

print ('men rows', len(men))
writ(menout, men)


"""
if float(lisp[4])  < filter2:
	continue
if float(lisp[1])  < filter3:
	continue
if (float(lisp[4]) + float(lisp[3]) ) < filter4:
	continue
if float(lisp[4]) < filter5 and float(lisp[3])< filter6:
	continue
if float(lisp[4]) < filter7 and float(lisp[3])< filter8:
	continue
"""




