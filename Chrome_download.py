# -*-edconding:euc-kr-*-
import pandas as pd
import sqlite3
import datetime
import os
from urllib import parse
from PyQt5.QtWidgets import *


def fixDate(timestamp):
    epoch_start = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=int(timestamp))
    return epoch_start + delta

os.system("taskkill.exe /f /im chrome.exe")

selectStatement = 'SELECT  DISTINCT downloads.target_path, downloads.referrer, downloads.start_time, downloads.end_time, downloads.received_bytes, downloads.opened, downloads.last_access_time,downloads.current_path ,downloads_url_chains.url, downloads.last_modified FROM downloads,downloads_url_chains WHERE downloads.id == downloads_url_chains.id'

username = os.getlogin()
historyFile = 'C:\\Users\\' + username + \
    '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'
c = sqlite3.connect(historyFile)
down_length = 0
localFileName = [] #로컬 열람파일이름
localFileTime = [] #로컬 열람 시간
localFileAddr = [] #로컬 열람 주소
downFileName = [] #다운로드파일이름
downFileAddr = [] #다운로드 파일주소
DownTime = [] #다운로드 시간
startDown = [] #다운시작시간
EDown = [] #다운끝난시간
DownSize = [] #다운로드받은 사이즈
downLastAccess = [] #마지막 접근시간
D_Addr = [] #다운로드 접속 주소
D_Time = [] #다운로드 접속 시각
'''
캐시 파일 다운로드 주소, 캐시파일 다운로드 시각은 없음
'''
for row in c.execute(selectStatement):
    localFile = row[7].split("\\")
    localFN = localFile[len(localFile) - 1:]
    localFileName = localFileName + localFN #로컬 열람파일이름
    #print(localFileName[down_length])
    localFileAddr.insert(down_length, row[7])
    if "1601-01-01 00:00:00" == str(fixDate(row[6])):
        localFileTime.insert(down_length,"")
    else:
        localFileTime.insert(down_length ,str(fixDate(row[6])))
    #print("localFileTime", localFileTime)
    downFile = row[0].split("\\")
    downFN = downFile[len(downFile) - 1:]
    downFileName = downFileName + downFN #파일이름
    downFileAddr.insert(down_length, row[0] )
    if "1601-01-01 00:00:00" == str(fixDate(row[2])):
        startDown.insert(down_length, "")
    else:
        startDown.insert(down_length, str(fixDate(row[2])).split(".")[0]) #다운시작시간
    if "1601-01-01 00:00:00" == str(fixDate(row[2])):
        EDown.insert(down_length, "")
    else:
        EDown.insert(down_length, str(fixDate(row[3])))
    DownTime.insert(down_length, startDown[down_length]+" ~ "+EDown[down_length])
    if row[6] == 0 :
        downLastAccess.insert(down_length, " ") #마지막 접근시간
    else :
        downLastAccess.insert(down_length, str(fixDate(row[6])).split(".")[0])
    DownSize.insert(down_length, str(row[4]))
    D_Addr.insert(down_length,  str(row[1]))
    #print(str(fixDate(row[6])))
    if "1601-01-01 00:00:00" == str(fixDate(row[6])):
        D_Time.insert(down_length, "")
    else:
        D_Time.insert(down_length, str(fixDate(row[6])))
    #print("D_time : ", D_Time[down_length])
    down_length += 1
#print(down_length)
#print(DownTime)
#print(D_Time)
#print(localFileTime)