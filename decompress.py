# -*- coding: UTF-8 -*-

import math
import wmi
import platform
import decom_xpress
import os, datetime
from datetime import datetime, timedelta
from main import *

def main():
    print("\nAchu Prefetch Parser")

def volume():
    serial = {}
    for volume in wmi.WMI().Win32_LogicalDisk():
        serial.setdefault(volume.VolumeSerialNumber, volume.Caption)
    return serial

def decom(input_file):
    try:  # Win10
        data = decom_xpress.decom(input_file)
        return data
    except Exception as e:
        print(e)

def LittleEndianToInt(buf):
    val = 0
    for i in range(0, len(buf)):
        multi = 1
        for j in range(0, i):
            multi *= 256
        val += buf[i] * multi
    return val

def time_convert(time):
    dd = time
    dt = '%016x' % dd
    us = int(dt, 16) / 10.
    return datetime(1601, 1, 1) + timedelta(microseconds=us) + timedelta(hours=9)  # UTC 9:00맞 추기

def time_change(buf):
    littleendian = buf
    bigendian = LittleEndianToInt(littleendian)
    return time_convert(int(bigendian))

def remove_null(bytearray_str): # 실행파일 경로 문제
    name_str = ""
    for i in range(0,math.ceil(len(bytearray_str))):
        if i%2 == 0:
            if str(bytearray_str[i]) != "0":
                name_str += chr(bytearray_str[i])
            else:
                continue
        else:
            continue
    return name_str

def version(number):
    if (int(number) == 30):
        return "Windows 10"

    elif (int(number) == 26):
        return "Windows 8.1"

    elif (int(number) == 23):
        if platform.release() == '7':
            return "Windows 7"
        else:
            return "Windows Vista"

    else:
        if platform.release() == "2003":
            return "Windows 2003"
        else:
            return "Windows XP"

def Timehistory(count, buf):
    Time_List = []
    a = []
    if count == 1:
        return a
    elif count < 9:
        for i in range(0, count-1):
            Time_List.append("RunTimeHistory" + str(i))
        minimum = 136
        maximum = 144
        for list in Time_List:
            globals()[list] = time_change(buf[minimum:maximum])
            minimum += 8
            maximum += 8

        for name in Time_List:
            a.append(globals()[name])
        return a

    elif count >= 9:
        for i in range(0, 7):
            Time_List.append("RunTimeHistory" + str(i))

        minimum = 136
        maximum = 144
        for list in Time_List:
            globals()[list] = time_change(buf[minimum:maximum])
            minimum += 8
            maximum += 8

        for name in Time_List:
            a.append(globals()[name])
        return a

dll_com_list = ""
def Dll_List(buf):
    section_c_offset = LittleEndianToInt(buf[100:103])
    section_d_offset = LittleEndianToInt(buf[108:111])
    dll_byte = buf[section_c_offset:section_d_offset]
    global dll_com_list
    dll_com_list = ""
    split_code = "\VOLUME"
    for n in range(0, int(len(dll_byte))):
        if n % 2 == 0:
            dll_com_list += chr(dll_byte[n])
    result = dll_com_list.split(split_code)
    for n in range(1, len(result)):
        if "\DEVICE" in result[n]:
            data = split_code + result[n].split("\DEVICE\\")[0]
        else:
            data1 = split_code + result[n]
    #print(dll_com_list)
    #print(type(dll_com_list))
    #print("data : ", data)
    #print("data1 :",data1)
    return dll_com_list

D_list = []

def pre_DLL():
    tmp1 = ""
    tmp2 = []
    tmp1 = dll_com_list
    D_list.clear()
    #print(tmp1)
    V_str = "\VOLUME"
    tmp2 = tmp1.split("\VOLUME")
    #print(tmp2)
    for i in tmp2[1:]:
        D_list.append(V_str + i)
    tmp1 = tmp1.split("\DEVICE\\")[0]
    #print(D_list)

def Full_Path(serial,pathlist,processname):
    fullpathname = ""
    fullpathlist = []
    pathlist = pathlist.split('\VOLUME')
    for i in pathlist:
        for key, value in serial.items():  # DLL list(참조목록) Fullpath,
            if key.lower() in i: # i volume 경로
                full_path_name = i.split("}")[-1]
                if "\\DEVICE"  in full_path_name:
                    continue
                else:
                    fullpathlist.append(value+full_path_name)

    for i in range(0, len(fullpathlist)):
        if processname in fullpathlist[i]:
            fullpathname = fullpathlist[i]
        else:
            continue

    return fullpathname
if __name__ == '__main__':
    main()
