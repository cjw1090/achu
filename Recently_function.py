from decompress import *
from datetime import datetime, timedelta
from operator import itemgetter
import os

total_result = []

def Recently(self):
    index = 0
    for path, dirs, files in os.walk(Ui_Dialog.path):
        for file in files:
            if os.path.splitext(file)[1].lower() in ['.pf']:
                target = path + '//' + file
                data = decom(target)
                try:
                    aa = parser(self, index, data, target, file)
                    index += 1
                    total_result.append(aa)
                except:
                    pass
    return total_result

def parser(self, index, buf, target, file):
    process_name = remove_null(buf[16:74])  # 실행파일 이름
    file_name = file  # 파일 이름
    file_size = LittleEndianToInt(buf[12:15])  # 파일 크기
    ctime = datetime.fromtimestamp(os.path.getctime(target))  # 생성시각
    mtime = datetime.fromtimestamp(os.path.getmtime(target))  # 수정시각
    last_runtime = time_change(buf[128:136])  # 마지막 실행시각
    run_count = LittleEndianToInt(buf[200:203])  # 실행 횟수
    str_ctime = str(ctime)
    str_mtime = str(mtime)
    str_last_runtime = str(last_runtime)
    str_runcount = run_count

    ctime_result = ""
    for a in str_ctime:
        if a != ".":
            ctime_result += a
        else:
            break

    mtime_result = ""
    for a in str_mtime:
        if a != ".":
            mtime_result += a
        else:
            break

    last_runtime_result = ""
    for a in str_last_runtime:
        if a != ".":
            last_runtime_result += a
        else:
            break

    total_result_list = [process_name, ctime_result, mtime_result, last_runtime_result, str_runcount]
    return total_result_list

def setdata(self,total_result):
    total_result.sort(key=itemgetter(4))

    length = len(total_result)

    indexing = length / 100 * 80
    indexing = math.floor(indexing)
    total_result_sum = 0

    while total_result_sum < indexing:
        total_result_sum = total_result_sum + 1
        total_result.pop(0)
        if total_result_sum == indexing:
            break

    total_result.sort(key=itemgetter(4), reverse=True)

    return total_result

