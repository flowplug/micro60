from operator import itemgetter as itg

menout = 'aamenbuyNVDA.csv'

filter1 = 0
filter2 = .94
filter3 = 1
filter4 = 1.0
filter5 = 0.90
filter6 = 0.02
filter7 = 0.96
filter8 = 0.09
filter9 = 0.98
def writ(fi,lii):
    fout = open (fi,'w')
    for ku in lii:
        fout.write(ku)

fintx = 'abuyNVDA.csv'
fin = open(fintx)
lis = fin.readlines()

print ('rows original matrix:', len(lis))
men = []
for li in lis:
	li=li.replace(',,',',') # Replaces the empty list entry before the column orders fields.
	li = li.replace('../live/','')
	lisp = li.split(',')
	if float(lisp[4]) == 1.0 and float(lisp[1]) > 0:
		men += [li]
		continue
	#if float(lisp[3]) == filter1: 
		#continue		
	if int(lisp[13]) < 9 and float(lisp[4]) > filter5:
		men += [li]
		continue
	if float(lisp[4]) < filter5 or float(lisp[1]) < 6:
		continue
	#if float(lisp[4]) >= filter5 and float(lisp[1]) >= 2:
		#men += [li]
		#continue				
	if float(lisp[4])  < filter2:
		continue
	if float(lisp[1])  < filter3:
		continue
	#if (float(lisp[4]) + float(lisp[3]) ) < filter4:
		#continue
	#if float(lisp[4]) < filter5 and float(lisp[3])< filter6:
		#continue
	#if float(lisp[4]) < filter7 and float(lisp[3])< filter8:
		#continue
	else:
		men += [li]

print ('men rows', len(men))
writ(menout, men)







