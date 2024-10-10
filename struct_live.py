
from numpy import zeros
import struct_calc

class mind(object):
    def __init__(self, ob):
        self.exc = struct_calc.calk(ob)
        self.calcl = zeros((len(self.exc.series_names.keys()), len(ob.rdi['live']['dtrue'])))
        self.varss = ob.avg_symbs
        self.focii = self.read_focii(ob)

    def read_focii(self,ob):
        focii = {}
        focii['tick_sec'] = ob.calc['tick_sec'].upper()
        focii['dex_sec'] = ob.calc['dex_sec'].upper()
        focii['crypto_tick_sec'] = ob.calc['crypto_tick_sec'].upper()
        focii['crypto_dex_sec'] = ob.calc['crypto_dex_sec'].upper()
        return focii

if __name__ == "__main__":
    import nov_admin
    import fig
    obb = fig.par()
    obb.add_list('conflate', obb.tre['conflate_fulln'])
    obb.add_list('conflate_fill', obb.tre['conflate_fill'])
    obx = nov_admin.symb(obb)
    ob = struct_calc.calk(obx)
    # print (ob.series_names)
    # sys.exit()
    # ob.cob = ob
    aa = mind(obx)

