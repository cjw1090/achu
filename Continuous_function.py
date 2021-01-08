from continue_1 import shimcacheParser, result1
from decompress import *

result = []

def ck(self, result):
    global total_count
    pre = []

    result.sort(key=lambda x: x[1])

    for i in range(0, len(result)):
        if(str(result[i][1]) != "1601-01-01 09:00:00"):
            date_time_i = datetime.strptime(result[i][1], '%Y-%m-%d %H:%M:%S')
            for j in range(i + 1, len(result)):
                date_time_j = datetime.strptime(result[j][1], '%Y-%m-%d %H:%M:%S')
                if (date_time_j - date_time_i).seconds < 60 and (date_time_j).day == (date_time_i).day:
                    if result[i] not in pre and result[j] not in pre:
                        pre.append(result[i])
                        pre.append(result[j])
                    elif result[i] not in pre and result[j] in pre:
                        pre.append(result[i])
                    elif result[i] in pre and result[j] not in pre:
                        pre.append(result[j])
                    else:
                        continue
    return pre

def ck1(self,sim):
    global total_count
    sim1 = []

    sim.sort(key=lambda x: x[1])

    for i in range(0, len(sim)):
        if(str(sim[i][1]) != "1601-01-01 09:00:00"):
            """
            if '.' in str(sim[i][1]):
                date_time_i = datetime.strptime(str(sim[i][1]).split('.')[0], '%Y-%m-%d %H:%M:%S')
            else:
                date_time_i = datetime.strptime(str(sim[i][1]), '%Y-%m-%d %H:%M:%S')
            """
            date_time_i = datetime.strptime(sim[i][1], '%Y-%m-%d %H:%M:%S')
            for j in range(i + 1, len(sim)):
                date_time_j = datetime.strptime(sim[j][1], '%Y-%m-%d %H:%M:%S')
                if (date_time_j - date_time_i).seconds < 60 and (date_time_j).day == (date_time_i).day:
                    if sim[i] not in sim1 and sim[j] not in sim1:
                        sim1.append(sim[i])
                        sim1.append(sim[j])
                    elif sim[i] not in sim1 and sim[j] in sim1:
                        sim1.append(sim[i])
                    elif sim[i] in sim1 and sim[j] not in sim1:
                        sim1.append(sim[j])
                    else:
                        continue
    return sim1