import nov_admin
import struct_calc
import fig
import strun_train
import sys

obb = fig.par()
obb.add_list('conflate', obb.tre['conflate_fullx'])
obb.add_list('conflate_fill', obb.tre['conflate_fillx'])
obx = nov_admin.symb(obb)
orb = struct_calc.calk(obx, True) # writes sequential column names in a file 
# /home/alan2/dev/cleandev/microtree/mat_csvs/column_names.txt if the
# second parameter is True.

strun_train.alg(orb, orb.cob.calc['train_targ'])


