import os
from PyQt5 import QtCore, QtGui, QtWidgets
import wmi
import os
import re

from winreg import *
from os.path import basename
import re, struct
from datetime import datetime, timedelta
import sys

net = "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\AppCompatCache"  # 서브레지스트리 목록 지정 ( ShimCache 경로 )
reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)  # 루트 레지스트리 핸들 객체 얻기
key = OpenKey(reg, net)  # 레지스트리 핸들 객체 얻기

a, b, c = EnumValue(key, 0)  # 지정한 레지스트리 하위 키값 조회
bin_size = len(b)

result1 = []

def shimcacheParser():
    result_tmp = []
    binary = b
    n = 0
    # 첫번째 0x34 =52값이 header사이즈로 보이니까 첫번째 값을 가져온다
    header_size = binary[0]
    # 헤더 크기 이후의 값을 바이너리로 다시 담는다
    while n < bin_size:
        bin = binary[n + header_size:]
        if not bin:
            break
        signature = bin[0:4].decode()
        unknown = bin[4:8].hex()
        entry_size = struct.unpack('L', bin[8:12])[0]
        path_len = struct.unpack('h', bin[12:14])[0]
        path_str = bin[14:path_len + 14].decode('UTF-16')
        filename = basename(path_str)

        time = bin[path_len + 14:path_len + 14 + 8].hex()
        times = time[14:16] + time[12:14] + time[10:12] + time[8:10] + time[6:8] + time[4:6] + time[2:4] + time[0:2]
        data_size = struct.unpack('i', bin[path_len + 22:path_len + 26])[0]
        data = bin[path_len + 14 + 12:path_len + 14 + 12 + data_size]
        n += path_len + 12 + 14 + data_size
        us = int(times, 16) / 10.

        result_time = datetime(1601, 1, 1) + timedelta(microseconds=us)
        s_time = str(result_time)
        if "1601-01-01 00:00:00" == s_time:
            continue
        else:
            s_time
        result_tmp = [filename, path_str, s_time, data_size, result_time]
        result1.append(result_tmp)

    return result1