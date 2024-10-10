

def glee(sqlrecs, ray, ob, dtrue ):
    for sy in ob.avg_symbs:
        for rec in sqlrecs[sy]:
            countt = dtrue.count(str(rec[1]))
            if countt == 0: continue
            lo = dtrue.index(str(rec[1]))
            for ou in range(2, len(ob.fields) + 2):
                ray[sy][(lo * len(ob.fields)) + ou - 2] = rec[ou]
