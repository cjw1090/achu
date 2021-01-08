import sqlite3, datetime,os

def fixDate(timestamp):
    epoch_start = datetime.datetime(1601,1,1)
    delta = datetime.timedelta(microseconds=int(timestamp))
    return epoch_start + delta

#print("\nAchu Chrome History\n")
os.system("taskkill.exe /f /im chrome.exe")
'''
username = os.getlogin()
path2 = "xcopy \"C:/Users/"+ username + "/AppData/Local/Google/Chrome/User Data/Default/History\" \"./history\" /s /e /h /d"
os.system(path2)
'''
selectStatement = 'SELECT urls.id, urls.url, urls.title, urls.visit_count, urls.last_visit_time, visits.visit_time FROM urls,visits where urls.id == visits.id;'
username = os.getlogin()
historyFile = 'C:\\Users\\' + username + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'
#historyFile = './history'
c = sqlite3.connect(historyFile)
history_length = 0
historyFileName = [] #히스토리 파일 이름(주소)
HisVisTime = [] #히스토리 접속 시간 (생성시간)
title = [] #접속주소타이틀
historyCount = [] # 히스토리 방문 횟수
historyLastAccess = [] # 히스토리 마지막 접근시간
'''
로컬 열람 파일 명 , 로컬 파일 열람 시각, 다운로드 파일 명, 다운로드 시각 ,캐시 파일 다운로드 주소, 캐시 파일 다운로드 시각 xxx
'''
for row in c.execute(selectStatement):
    #addr = str(row[1])[len(str(row[1])) - 1:]
    historyFileName.insert(history_length, str(row[1]))
    HisVisTime.insert(history_length, str(fixDate(row[5])).split(".")[0])
    historyCount.insert(history_length, row[3])
    title.insert(history_length,str(row[2]) )
    historyLastAccess.insert(history_length, str(fixDate(row[4])).split(".")[0])
    history_length += 1
    '''
    print("사용 웹 브라우저 : Chrome")
    print("로컬 열람 파일 명 : ")
    print("로컬 파일 열람 시각 : ")
    print("다운로드 파일 명 : ")
    print("다운로드 시각 : ")
    print("사이트 접속 주소 : ")
    print("\t주소 : ", str(row[1]))
    print("\t타이틀 : ", str(row[2]))
    print("\t방문 횟수 : ", row[3])
    print("사이트 접속 시각 : ")
    print("\t접속 시각 : ",str(fixDate(row[5])))
    print("\t마지막 접속 시각 : ", str(fixDate(row[4])))
    print("캐시 파일 다운로드 주소 : ")
    print("캐시 파일 다운로드 시각 : ")
    print ("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
    '''
