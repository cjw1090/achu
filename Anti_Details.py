# -*- coding: utf-8 -*-
import math
import os
from datetime import datetime, timedelta
import hashlib
from winreg import *
from os.path import basename
import struct

import wmi
from PyQt5 import QtCore, QtGui, QtWidgets
import csv

import decom_xpress
import decompress

file_name_1=""
process_name_1=""
process_path_3=""
ctime_1=""
mtime_1=""
last_runtime_1=""
run_count_1=""
timehistory=""
existence=""
count = 0

class Ui_Dialog(object):

    def files_count(self):
        return len(os.listdir(Ui_Dialog.path))

    def setupUi(self, tab, tapname_list):
        global count
        count = 0
        self.net = "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\AppCompatCache"  # 서브레지스트리 목록 지정 ( ShimCache 경로 )
        self.reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)  # 루트 레지스트리 핸들 객체 얻기
        self.key = OpenKey(self.reg, self.net)  # 레지스트리 핸들 객체 얻기
        self.a, self.b, self.c = EnumValue(self.key, 0)  # 지정한 레지스트리 하위 키값 조회
        self.bin_size = len(self.b)

        font = QtGui.QFont()
        font.setFamily("돋움")
        font.setBold(False)
        font.setWeight(50)
        font.setPointSize(9)

        font1 = QtGui.QFont()
        font1.setFamily("Agency FB")
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setWeight(75)

        self.gridLayout_5 = QtWidgets.QGridLayout(tab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_6 = QtWidgets.QGridLayout(tab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout = QtWidgets.QGridLayout()

        self.AntiTable = QtWidgets.QTableWidget(tab)
        self.gridLayout_5.addWidget(self.AntiTable, 0, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.AntiTable.setFont(font)
        self.AntiTable.setMouseTracking(False)
        self.AntiTable.setTabletTracking(False)
        self.AntiTable.setAcceptDrops(False)
        self.AntiTable.setToolTipDuration(-1)
        self.AntiTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.AntiTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.AntiTable.setAutoScroll(True)
        self.AntiTable.setAutoScrollMargin(16)
        self.AntiTable.setSortingEnabled(True)
        self.AntiTable.setShowGrid(True)
        self.AntiTable.setRowCount(1000)
        self.AntiTable.setColumnCount(9)
        self.AntiTable.setObjectName("AntiTable")
        self.AntiTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)  # Options : Not Edit
        self.AntiTable.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)  # Select Rows


        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.AntiTable.setHorizontalHeaderItem(0, item)
        self.AntiTable.setColumnWidth(0, 85)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.AntiTable.setHorizontalHeaderItem(1, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.AntiTable.setHorizontalHeaderItem(2, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.AntiTable.setHorizontalHeaderItem(3, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.AntiTable.setHorizontalHeaderItem(4, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.AntiTable.setHorizontalHeaderItem(5, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.AntiTable.setHorizontalHeaderItem(6, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.AntiTable.setHorizontalHeaderItem(7, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.AntiTable.setHorizontalHeaderItem(8, item)

        _translate = QtCore.QCoreApplication.translate
        tapname_list.append(self.AntiTable.objectName())
        self.AntiTable.setHorizontalHeaderLabels(
            ["Existence", "File Name", "Process Name", "Process Path", "Create Time", \
             "Modified Time", "Last Run Time", "Run Time", "Run Count"])

        header = self.AntiTable.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        for i in range(2, self.AntiTable.columnCount() - 1):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        bi = bi_Dialog()
        t = 1
        path = "C:\\Windows\\Prefetch"  # 프리패치 경로
        for path, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1].lower() in ['.pf']:  # 해당 경로에서 .pf 확장자 갖는 file 찾기
                    for key, value in antiDB.items():
                        key_2 = key.split('.')[0]
                        file_2 = file.lower()
                        if file_2.find(key_2) != -1:
                            target = path + '//' + file
                            print(t)
                            data = decompress.decom(target)
                            try:
                                a, b, c, d, e, f, g, h, i = parser(data, target, file)
                                self.AntiTable.setItem(count, 0, QtWidgets.QTableWidgetItem(a))
                                self.AntiTable.setItem(count, 1, QtWidgets.QTableWidgetItem(b))
                                self.AntiTable.setItem(count, 2, QtWidgets.QTableWidgetItem(c))
                                self.AntiTable.setItem(count, 3, QtWidgets.QTableWidgetItem(d))
                                self.AntiTable.setItem(count, 4, QtWidgets.QTableWidgetItem(e))
                                self.AntiTable.setItem(count, 5, QtWidgets.QTableWidgetItem(f))
                                self.AntiTable.setItem(count, 6, QtWidgets.QTableWidgetItem(g))
                                self.AntiTable.setItem(count, 7, QtWidgets.QTableWidgetItem(i))
                                self.AntiTable.setItem(count, 8, QtWidgets.QTableWidgetItem(h))
                                count += 1
                            except:
                                pass
                            t += 1
        f = open('write.csv', 'r', -1, 'utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            for key, value in antiDB.items():
                process_name_2 = line[6].lower()
                if process_name_2.find(key) == 0:
                    if value == getHash(line[13]):
                        output = ["", line[1], line[14], line[11], line[3], line[4], line[5]]
                        print(output)
                        self.AntiTable.setItem(count, 0, QtWidgets.QTableWidgetItem(""))
                        self.AntiTable.setItem(count, 1, QtWidgets.QTableWidgetItem(line[1]))
                        self.AntiTable.setItem(count, 2, QtWidgets.QTableWidgetItem(line[6]))
                        self.AntiTable.setItem(count, 3, QtWidgets.QTableWidgetItem(line[13]))
                        self.AntiTable.setItem(count, 4, QtWidgets.QTableWidgetItem(line[3]))
                        self.AntiTable.setItem(count, 5, QtWidgets.QTableWidgetItem(line[4]))
                        self.AntiTable.setItem(count, 6, QtWidgets.QTableWidgetItem(line[5]))
                        self.AntiTable.setItem(count, 7, QtWidgets.QTableWidgetItem(""))
                        self.AntiTable.setItem(count, 8, QtWidgets.QTableWidgetItem(""))
                        count = count + 1
                    elif getHash(line[13]) == 1:
                        output = ["N", line[1], line[14], line[11], line[3], line[4], line[5]]
                        print(output)
                        self.AntiTable.setItem(count, 0, QtWidgets.QTableWidgetItem("N"))
                        self.AntiTable.setItem(count, 1, QtWidgets.QTableWidgetItem(line[1]))
                        self.AntiTable.setItem(count, 2, QtWidgets.QTableWidgetItem(line[6]))
                        self.AntiTable.setItem(count, 3, QtWidgets.QTableWidgetItem(line[13]))
                        self.AntiTable.setItem(count, 4, QtWidgets.QTableWidgetItem(line[3]))
                        self.AntiTable.setItem(count, 5, QtWidgets.QTableWidgetItem(line[4]))
                        self.AntiTable.setItem(count, 6, QtWidgets.QTableWidgetItem(line[5]))
                        self.AntiTable.setItem(count, 7, QtWidgets.QTableWidgetItem(""))
                        self.AntiTable.setItem(count, 8, QtWidgets.QTableWidgetItem(""))
                        count = count + 1
        f.close()

        cachedatas = bi.shimcacheParser()
        for cachedata in cachedatas:
            for key, value in antiDB.items():
                process_name_2 = cachedata[0].lower()
                if process_name_2.find(key) == 0:
                    if value == getHash(cachedata[1]):
                        output = ["", "", cachedata[0], cachedata[1], "", cachedata[2], "", "", ""]
                        print(output)
                        self.AntiTable.setItem(count, 0, QtWidgets.QTableWidgetItem(""))
                        self.AntiTable.setItem(count, 1, QtWidgets.QTableWidgetItem(""))
                        self.AntiTable.setItem(count, 2, QtWidgets.QTableWidgetItem(cachedata[0]))
                        self.AntiTable.setItem(count, 3, QtWidgets.QTableWidgetItem(cachedata[1]))
                        self.AntiTable.setItem(count, 4, QtWidgets.QTableWidgetItem(""))
                        self.AntiTable.setItem(count, 5, QtWidgets.QTableWidgetItem(cachedata[2]))
                        self.AntiTable.setItem(count, 6, QtWidgets.QTableWidgetItem(""))
                        self.AntiTable.setItem(count, 7, QtWidgets.QTableWidgetItem(""))
                        self.AntiTable.setItem(count, 8, QtWidgets.QTableWidgetItem(""))
                        count += 1
                    elif getHash(cachedata[1]) == 1:
                        output = ["N", "", cachedata[0], cachedata[1], "", cachedata[2], "", "", ""]
                        print(output)
                        self.AntiTable.setItem(count, 0, QtWidgets.QTableWidgetItem("N"))
                        self.AntiTable.setItem(count, 1, QtWidgets.QTableWidgetItem(""))
                        self.AntiTable.setItem(count, 2, QtWidgets.QTableWidgetItem(cachedata[0]))
                        self.AntiTable.setItem(count, 3, QtWidgets.QTableWidgetItem(cachedata[1]))
                        self.AntiTable.setItem(count, 4, QtWidgets.QTableWidgetItem(""))
                        self.AntiTable.setItem(count, 5, QtWidgets.QTableWidgetItem(cachedata[2]))
                        self.AntiTable.setItem(count, 6, QtWidgets.QTableWidgetItem(""))
                        self.AntiTable.setItem(count, 7, QtWidgets.QTableWidgetItem(""))
                        self.AntiTable.setItem(count, 8, QtWidgets.QTableWidgetItem(""))
                        count += 1
        self.AntiTable.setRowCount(count)

class bi_Dialog(object):
    def files_count(self):
        return len(os.listdir(Ui_Dialog.path))

    def __init__(self):
        self.net = "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\AppCompatCache"  # 서브레지스트리 목록 지정 ( ShimCache 경로 )
        self.reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)  # 루트 레지스트리 핸들 객체 얻기
        self.key = OpenKey(self.reg, self.net)  # 레지스트리 핸들 객체 얻기

        self.a, self.b, self.c = EnumValue(self.key, 0)  # 지정한 레지스트리 하위 키값 조회
        self.bin_size = len(self.b)

    def shimcacheParser(self):
        result = []
        result_tmp = []
        self.binary = self.b
        # print(bin_size)
        self.n = 0
        # 첫번째 0x34 =52값이 header사이즈로 보이니까 첫번째 값을 가져온다
        self.header_size = self.binary[0]
        # 헤더 크기 이후의 값을 바이너리로 다시 담는다
        while self.n < self.bin_size:
            self.bin = self.binary[self.n + self.header_size:]
            if not self.bin:
                break
            signature = self.bin[0:4].decode()
            unknown = self.bin[4:8].hex()
            entry_size = struct.unpack('L', self.bin[8:12])[0]
            path_len = struct.unpack('h', self.bin[12:14])[0]
            path_str = self.bin[14:path_len + 14].decode('UTF-16')
            filename = basename(path_str)

            time = self.bin[path_len + 14:path_len + 14 + 8].hex()
            times = time[14:16] + time[12:14] + time[10:12] + time[8:10] + time[6:8] + time[4:6] + time[2:4] + time[0:2]
            data_size = struct.unpack('i', self.bin[path_len + 22:path_len + 26])[0]
            data = self.bin[path_len + 14 + 12:path_len + 14 + 12 + data_size]
            self.n += path_len + 12 + 14 + data_size
            us = int(times, 16) / 10.

            result_time = datetime(1601, 1, 1) + timedelta(microseconds=us)
            s_time = str(result_time)
            if "1601-01-01 00:00:00" == s_time:
                s_time = "Unknown Time"
            else:
                s_time
            result_tmp = [filename, path_str, s_time]
            result.append(result_tmp)
            # result_tmp=[]
        return result

def guess_encoding(csv_file): #utf-8 인코딩 관련
    """guess the encoding of the given file"""
    import io
    import locale
    with io.open(csv_file, "rb") as f:
        data = f.read(5)
    if data.startswith(b"\xEF\xBB\xBF"):
        return "utf-8-sig"
    elif data.startswith(b"\xFF\xFE") or data.startswith(b"\xFE\xFF"):
        return "utf-16"
    else:
        try:
            with io.open(csv_file, encoding="utf-8") as f:
                preview = f.read(222222)
                return "utf-8"
        except:
            return locale.getdefaultlocale()[1]


def getHash(path, blocksize=65536): #실행파일 해시값 계산
    try:
        afile = open(path, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)

        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)

        afile.close()
        return hasher.hexdigest()
    except:
        return 1

antiDB = {
"ccleaner.exe" : "e66875f3da6996126360240f0bd38c79",
"ccleaner64.exe" : "c9be8f1bf9690ce30b609858601a3ef3",
"bcwipe.exe" : "5037b74bc42053fe9909cf3cd92c9e50",
#"alzip.exe" : "6e4b1760fa0ca755395a269a6a8def62",
#"chrome.exe" : "90c30632b1d34656235a1aabc9ec9860",
"eraser.exe" : "68986218d96d737e32b361240a3e7ce4",
"sdelete.exe" : "f41a1afc4cfb95f35cd92da98d90c27b",
"sdelete64.exe" : "2b5cb081721b8ba454713119be062491",
"antirecovery.exe" : "b7ef0b8c34dbafdd529816826b1ed31b",
"fileshredder.exe" : "e3a96844aeaa899413721c4dd8b392de",
"slimcleanerPlus.exe" : "486cc9a8caa49e2422458035ad77d90a",
"cybershredder.exe" : "c039c213f1cbbc329be9ecceff072444",
"drivecleanser.exe" : "56e61a8c22b4c62ad4761ce283d40476",
"ee.exe" : "3b3afb201f39f35e51877ca91ab2d5d3",
"truecrypt.exe" : "03316ed8bd428007777ab5785a33fab4",
"veracrypt.exe" : "e044b57200d0edb5eeecd54238884422",
"axcrypt.exe" : "cc6bde6b008ec89c1b0b385526422c04",
"freeotfe.exe" : "08c1effa1d2590811c687bcd851919e8",
"openpuff.exe" : "f250614a3ed5c83c84359a26ec29a276",
"s-tools.exe" : "e245319bdb383c5a3a65de238e6b25f1"
}

def parser(buf, target, file):
    global file_name_1, process_name_1, process_path_3, ctime_1, mtime_1, last_runtime_1, run_count_1, timehistory, existence
    file_name = file  # 파일 이름
    process_name = decompress.remove_null(buf[16:74]) #실행파일 이름
    ctime = datetime.fromtimestamp(os.path.getctime(target)) #생성시각
    mtime = datetime.fromtimestamp(os.path.getmtime(target)) #수정시각
    last_runtime = decompress.time_change(buf[128:136]) #마지막 실행시각
    run_count = decompress.LittleEndianToInt(buf[200:203]) #실행횟수
    decompress.Dll_List(buf)
    process_path = decompress.Full_Path(decompress.volume(), decompress.Dll_List(buf), process_name)
    process_path_1 = process_path[0]
    process_path_2 = process_path_1[:-1] #실행파일 경로
    Pass_file_Name = process_path_2.split('\\')
    Pass_file_Name_1 = Pass_file_Name[-1]
    Pass_file_Name_2 = Pass_file_Name_1.lower()

    for key, value in antiDB.items():
        process_name_2 = process_name.lower()
        if process_name_2.find(key) == 0:
            if value == getHash(process_path_2):
                print("Process Name :", process_name)
                process_name_1 = process_name
                print("File Name :", file_name)
                file_name_1 = file_name
                process_path_3 = process_path_2
                ctime_1 = str(ctime).split(".")[0]
                mtime_1 = str(mtime).split(".")[0]
                last_runtime_1 = str(last_runtime).split(".")[0]
                run_count_1 = str(run_count)
                timehistory = str(Timehistory(run_count, buf)).split(".")[0]
                existence = ""
                return existence, file_name_1, process_name_1, process_path_3, ctime_1, mtime_1, last_runtime_1, run_count_1, timehistory
            elif getHash(process_path_2) == 1:
                print("Process Name :", process_name)
                process_name_1 = process_name
                print("File Name :", file_name)
                file_name_1 = file_name
                process_path_3 = process_path_2
                ctime_1 = str(ctime).split(".")[0]
                mtime_1 = str(mtime).split(".")[0]
                last_runtime_1 = str(last_runtime).split(".")[0]
                run_count_1 = str(run_count)
                timehistory = str(Timehistory(run_count, buf)).split(".")[0]
                existence = "N"
                return existence, file_name_1, process_name_1, process_path_3, ctime_1, mtime_1, last_runtime_1, run_count_1, timehistory

def volume(): #볼륨 값
    serial = {}
    for volume in wmi.WMI().Win32_LogicalDisk():
        serial.setdefault(volume.VolumeSerialNumber, volume.Caption)
    return serial


def decom(input_file): #decom_xpress.py(압축해제)파일 가져오기
    try:
        data = decom_xpress.decom(input_file)
        return data
    except Exception as e:
        print(e)


def LittleEndianToInt(buf): #리틀엔디언 변환
    val = 0
    for i in range(0, len(buf)):
        multi = 1
        for j in range(0, i):
            multi *= 256
        val += buf[i] * multi
    return val


def time_convert(time): #UTC+9:00
    dd = time
    dt = '%016x' % dd
    us = int(dt, 16) / 10.
    return datetime(1601, 1, 1) + timedelta(microseconds=us) + timedelta(hours=9)


def time_change(buf): #리틀엔디언 -> 빅엔디언 시간 변환
    littleendian = buf
    bigendian = LittleEndianToInt(littleendian)
    return time_convert(int(bigendian))

def remove_null(bytearray_str): #실행파일 경로 문제 (0값)
    name_str = ""
    for i in range(0, math.ceil(len(bytearray_str))):
        if i % 2 == 0:
            if str(bytearray_str[i]) != "0":
                name_str += chr(bytearray_str[i])
            else:
                continue
        else:
            continue
    return name_str

def Timehistory(count, buf): #실행이력
    Time_List = []
    result = ""
    if count == 1:
        return
    elif count < 9:
        for i in range(0, count - 1):
            Time_List.append("RunTimeHistory" + str(i))
        minimum = 136
        maximum = 144
        for list in Time_List:
            globals()[list] = time_change(buf[minimum:maximum])
            minimum += 8
            maximum += 8

        for name in Time_List:
            print(name, "=", globals()[name])
            if name == Time_List[0]:
                result = str(globals()[name])
            else:
                result = result + ", " + str(globals()[name])

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
            print(name, "=", globals()[name])
            if name == Time_List[0]:
                result = str(globals()[name])
            else:
                result = result + ", " + str(globals()[name])
    return result


def Dll_List(buf): #참조목록
    section_c_offset = LittleEndianToInt(buf[100:103])
    section_d_offset = LittleEndianToInt(buf[108:111])
    dll_byte = buf[section_c_offset:section_d_offset]
    dll_com_list = ""
    split_code = "\VOLUME"
    for n in range(0, int(len(dll_byte))):
        if n % 2 == 0:
            dll_com_list += chr(dll_byte[n])
    result = dll_com_list.split(split_code)
    for n in range(1, len(result)):
        if "\DEVICE" in result[n]:
            test_1 = split_code + result[n].split("\DEVICE\\")[0]
        else:
            test_2 = split_code + result[n]
    return dll_com_list


def Full_Path(serial, pathlist, processname): #참조목록 Fullpath
    fullpathlist = []
    pathlist = pathlist.split('\VOLUME')
    for i in pathlist:
        for key, value in serial.items():
            if key:
                if key.lower() in i:
                    full_path_name = i.split("}")[-1]
                    index_number = full_path_name.find(processname)
                    if index_number != -1:
                        fullpathlist.append(value + full_path_name)
                        fullpath = value + full_path_name
                        # print("DLL List Full Path : ", fullpath)
                    else:
                        fullpath = value + full_path_name
                        # print("DLL List Full Path : ", fullpath)
    return fullpathlist


def guess_encoding(csv_file): #utf-8 인코딩 관련
    """guess the encoding of the given file"""
    import io
    import locale
    with io.open(csv_file, "rb") as f:
        data = f.read(5)
    if data.startswith(b"\xEF\xBB\xBF"):
        return "utf-8-sig"
    elif data.startswith(b"\xFF\xFE") or data.startswith(b"\xFE\xFF"):
        return "utf-16"
    else:
        try:
            with io.open(csv_file, encoding="utf-8") as f:
                preview = f.read(222222)
                return "utf-8"
        except:
            return locale.getdefaultlocale()[1]


def getHash(path, blocksize=65536): #실행파일 해시값 계산
    try:
        afile = open(path, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)

        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)

        afile.close()
        return hasher.hexdigest()
    except:
        return 1

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.search()
    ui.shimcacheWrite()
    Dialog.show()
    sys.exit(app.exec_())