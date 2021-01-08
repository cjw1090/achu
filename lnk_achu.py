from datetime import datetime, timedelta
import binascii
import sys
import os
import csv

lnk_length = "13"
lnk_len = 1

# UTC 기준 Windows 64Bit 시간으로 변환
def convert_UTC(x):
    us = int(x, 16) / 10.
    y = datetime(1601, 1, 1) + timedelta(microseconds=us)
    return y


# 리스트 역순으로 뒤집은 후 합치는 함수(문자열화)
def reverse_and_combine(x):
    x.reverse()
    y = ''.join(x)
    return y


def divide_list(l, n):
    # 리스트 l의 길이가 n이면 계속 반복
    for i in range(0, len(l), n):
        yield l[i:i + n]


# 10진수를 2진수로 변환
def ten_to_two(insert):
    res = ""
    while True:
        x, y = divmod(insert, 2)
        res += str(y)

        if x < 2:
            res += str(x)
            break
        insert = x
    return res

# 시간 소수점 제거
def cut(a):
    b = a.split('.')[0]
    return b

class lnk_class:
    def __init__(self):
        self.LinkFile = ""
        self.LinkFile_Name = ""
        self.File_Size = ""
        self.ctime = ""
        self.mtime = ""
        self.atime = ""

        self.LinkFile_Size_3 = ""
        self.Creation_time_3 = ""
        self.Access_time_3 = ""
        self.Write_time_3 = ""

        self.Drive_Type_3 = ""
        self.Drive_Serial_Number_2 = ""
        self.Local_Base_Path_3 = ""
        self.Original_File_Name_1 = ""
        self.MAC_ADD = ""
        self.MAC_ADD_2 = ""
        self.NetBios_3 = ""


    def lnk(self, LinkFile, LinkFile_Name):
        global lnk_len
        #print("==========================================================================")
        self.LinkFile_Name = LinkFile_Name
        #print("FileName = ", LinkFile_Name)

        # 파일 사이즈 출력
        self.File_Size = str(round((os.path.getsize(LinkFile))/1024,2))
        # print("FileSize = ", LinkFile_Size, "byte")

        # create time을 타임 스탬프로 출력
        ctime_1 = os.path.getctime(LinkFile)
        ctime_2 = str(datetime.utcfromtimestamp(ctime_1))
        self.ctime = cut(ctime_2)
        #print("Create_Time = ", self.ctime)
        # modify time을 타임 스탬프로 출력
        mtime_1 = os.path.getmtime(LinkFile)
        mtime_2 = str(datetime.utcfromtimestamp(mtime_1))
        self.mtime = cut(mtime_2)
        #print("Modify_Time = ", self.mtime)
        # 마지막 access time을 타임 스탬프로 출력
        atime_1 = os.path.getatime(LinkFile)
        atime_2 = str(datetime.utcfromtimestamp(atime_1))
        self.atime = cut(atime_2)
        #print("Access_Time = ", self.atime)
        #print('\t')

        with open(LinkFile, 'rb') as f:
            content = f.read()

        res = binascii.hexlify(content)
        # print(res[152:156])

        # byte형을 문자열로 변환
        res_1 = res.decode('utf-8')

        # 2byte씩 list로 분류하기
        length = 2
        hex_D = [''.join(x) for x in zip(*[list(res_1[z::length]) for z in range(length)])]
        # print(hex_D)

        # 52는 File_Size 영역 이전까지 1h당 개수(52h)
        LinkFile_Size_1 = hex_D[52:52 + 4]
        LinkFile_Size_1.reverse()
        # 리스트를 문자열로 합치기
        LinkFile_Size_2 = ''.join(LinkFile_Size_1)
        self.LinkFile_Size_3 = str(round((int(LinkFile_Size_2, 16))/1024,2))
        #print("LinkFile_Size :", self.LinkFile_Size_3, "byte")

        # 생성 시간 구하기
        Creation_time_1 = hex_D[28:28 + 8]
        Creation_time_2 = reverse_and_combine(Creation_time_1)
        #print(Creation_time_2)
        # 생성시간 UTC 시간으로 변환
        if Creation_time_2 != "0000000000000000":
            self.Creation_time_3 = cut(str(convert_UTC(Creation_time_2)))
        #print("Original Creation_Time :", self.Creation_time_3)

        # 수정시간 구하기
        Write_time_1 = hex_D[44:44 + 8]
        Write_time_2 = reverse_and_combine(Write_time_1)
        # 수정시간 UTC 시간으로 변환
        if Write_time_2 != "0000000000000000":
            self.Write_time_3 = cut(str(convert_UTC(Write_time_2)))
        #print("Original Write_Time :", self.Write_time_3)

        # 접근시간 구하기
        Access_time_1 = hex_D[36:36 + 8]
        Access_time_2 = reverse_and_combine(Access_time_1)
        # 접근시간 UTC 시간으로 변환
        if Access_time_2 != "0000000000000000":
            self.Access_time_3 = cut(str(convert_UTC(Access_time_2)))
        #print("Original Access_Time :", self.Access_time_3)

        # 리틀엔디안 방식이므로 IDListSize를 뒤집어 준 후 합침
        # 합친 후 16진수를 10진수로 변환하여 사이즈 측정
        IDListSize_1 = res[154:156] + res[152:154]
        self.IDListSize_2 = int(IDListSize_1, 16)
        # print("IDListSize : ", self.IDListSize_2)

        # LinkFlags 없는 것 거르기
        LinkFlags_filter_1 = int(hex_D[20], 16)
        # print(LinkFlags_1)
        LinkFlags_filter = ten_to_two(LinkFlags_filter_1)
        # print(LinkFlags)
        if LinkFlags_filter[1] == "0":
            return

        # 0~151(152)은 ShellLinkHeader, 이후 152~155(4byte)는 IDListSize 크기를 알려준다.
        Start_LinkInfo_Num = 152 + 4 + (self.IDListSize_2 * 2)
        # print(Start_LinkInfo_Num)
        Start_LinkInfo = res[Start_LinkInfo_Num:]
        # print(Start_LinkInfo)

        # Drive_Type을 출력하기 위한 정보
        DRIVE_UNKNOWN = "Unknown"
        DRIVE_NO_ROOT_DIR = "No root directory"
        DRIVE_REMOVABLE = "Removable"
        DRIVE_FIXED = "Fixed (Hard disk)"
        DRIVE_REMOTE = "Remote (Network drive)"
        DRIVE_CDROM = "CD-ROM"
        DRIVE_RAMDISK = "Ram disk"

        # 드라이브 형식을 구분하기 위한 함수
        def DRIVE_TYPES(x):
            return \
                {0: DRIVE_UNKNOWN, 1: DRIVE_NO_ROOT_DIR, 2: DRIVE_REMOVABLE, 3: DRIVE_FIXED, 4: DRIVE_REMOTE,
                 5: DRIVE_CDROM,
                 6: DRIVE_RAMDISK}[x]

        # LinkInfo구간에서 Drive_Type 전까지 64개가 있으므로 65번째를 출력해야함. 0 -> 1번째 64 -> 65번째
        Drive_Type_1 = Start_LinkInfo[64:66]
        # print(Drive_Type_1)
        Drive_Type_2 = Drive_Type_1[1:]
        self.Drive_Type_3 = DRIVE_TYPES(int(Drive_Type_2))
        #print("Drive_Volume_Type :", self.Drive_Type_3)

        # 볼륨 시리얼 넘버
        Drive_Serial_Number_1 = Start_LinkInfo[78:80] + Start_LinkInfo[76:78] + Start_LinkInfo[74:76] + Start_LinkInfo[
                                                                                                        72:74]
        self.Drive_Serial_Number_2 = str(int(Drive_Serial_Number_1, 16))
        #print("Drive_Volume_Serial_Number :", self.Drive_Serial_Number_2)

        # Local_Base_Path 위치를 알기 위해선 LinkInfo 사이즈를 알아야 함.
        LinkInfoSize_1 = Start_LinkInfo[:2]
        LinkInfoSize_2 = int(LinkInfoSize_1, 16)
        # print("LinkInfoSize :", LinkInfoSize_2)

        VolumeIDSize_1 = Start_LinkInfo[56:58]
        VolumeIDSize_2 = int(VolumeIDSize_1, 16)
        # print("VolumeIDSize : ", VolumeIDSize_2)

        Start_Local_Base_Path = 56+(VolumeIDSize_2*2)
        # print(Start_Local_Base_Path)

        Find_End_Point = 0
        for i in range(0, 200, 2):
            Find_End_Point_1 = Start_LinkInfo[Start_Local_Base_Path+i:Start_Local_Base_Path+i+2]
            Find_End_Point_2 = int(Find_End_Point_1, 16)
            # print(Find_End_Point_2)
            if Find_End_Point_2 == 0 or Find_End_Point_2 > 127 :
                Find_End_Point = Start_Local_Base_Path+i
                # print(Find_End_Point)
                break

        Local_Base_Path_1 = Start_LinkInfo[Start_Local_Base_Path:Find_End_Point]
        # print(Local_Base_Path_1)
        Local_Base_Path_2 = Local_Base_Path_1.decode('utf-8')
        # print(Local_Base_Path_2)
        self.Local_Base_Path_3 = ''.join(
            [chr(int(''.join(c), 16)) for c in zip(Local_Base_Path_2[0::2], Local_Base_Path_2[1::2])])
        #print("Local_Base_Path :", self.Local_Base_Path_3)

        Original_File_Name = self.Local_Base_Path_3.split('\\')
        self.Original_File_Name_1 = Original_File_Name[-1]
        # print("Original_File_Name :", Original_File_Name[-1])
        #print('\t')

        # ShellLinkHeader 사이즈&Start point 찾기
        ShellLinkHeader_Size_1 = hex_D[0]
        ShellLinkHeader_Size = int(ShellLinkHeader_Size_1, 16)

        # LinkTargetIDList 사이즈 & Start point 찾기
        LinkTargetIDList_Size_1 = hex_D[ShellLinkHeader_Size:ShellLinkHeader_Size + 2]
        LinkTargetIDList_Size_2 = reverse_and_combine(LinkTargetIDList_Size_1)
        # LinkTargetIDList에는 마지막 2byte가 추가됨.
        LinkTargetIDList_Size = int(LinkTargetIDList_Size_2, 16) + 2
        # print("LinkTargetIDList Size :", LinkTargetIDList_Size)
        LinkInfo_Start_point = LinkTargetIDList_Size + ShellLinkHeader_Size
        # print("LinkInfo Start_point :", LinkInfo_Start_point)

        # LinkInfo 사이즈 & Start point 찾기
        LinkInfo_Size_1 = hex_D[LinkInfo_Start_point:LinkInfo_Start_point + 2]
        LinkInfo_Size_2 = reverse_and_combine(LinkInfo_Size_1)
        LinkInfo_Size = int(LinkInfo_Size_2, 16)
        # print("LinkInfo Size :", LinkInfo_Size)
        sExtraData_Start_point = LinkInfo_Start_point + LinkInfo_Size
        # print("sExtraData Start_point :", sExtraData_Start_point)

        # LinkFlag 존재여부 확인
        LinkFlags_1 = int(hex_D[20], 16)
        # print(LinkFlags_1)
        LinkFlags_2 = ten_to_two(LinkFlags_1)
        # print(LinkFlags_2)

        # NAME_STRING
        if LinkFlags_2[2] == "1":
            NAME_STRING_Size_1 = hex_D[sExtraData_Start_point:sExtraData_Start_point + 2]
            NAME_STRING_Size_2 = reverse_and_combine(NAME_STRING_Size_1)
            NAME_STRING_Size = (int(NAME_STRING_Size_2, 16) * 2) + 2
            # print(NAME_STRING_Size)
            sExtraData_Start_point += NAME_STRING_Size
            # print(sExtraData_Start_point)

        # Relative_path
        if LinkFlags_2[3] == "1":
            Size_1 = hex_D[sExtraData_Start_point:sExtraData_Start_point + 2]
            Size_2 = reverse_and_combine(Size_1)
            Size = (int(Size_2, 16) * 2) + 2
            # print("Relative_path Size :", Size)
            sExtraData_Start_point += Size
            # print(sExtraData_Start_point)

        # Working_DIR
        if LinkFlags_2[4] == "1":
            Size_1 = hex_D[sExtraData_Start_point:sExtraData_Start_point + 2]
            Size_2 = reverse_and_combine(Size_1)
            Size = (int(Size_2, 16) * 2) + 2
            # print("Working_DIR Size :", Size)
            sExtraData_Start_point += Size
            # print(sExtraData_Start_point)

        # COMMAND_LINE_ARGUMENTS
        if LinkFlags_2[5] == "1":
            Size_1 = hex_D[sExtraData_Start_point:sExtraData_Start_point + 2]
            Size_2 = reverse_and_combine(Size_1)
            Size = (int(Size_2, 16) * 2) + 2
            # print("ARGUMENTS Size :", Size)
            sExtraData_Start_point += Size
            # print(sExtraData_Start_point)

        # ICON_LOCATION
        if LinkFlags_2[6] == "1":
            Size_1 = hex_D[sExtraData_Start_point:sExtraData_Start_point + 2]
            Size_2 = reverse_and_combine(Size_1)
            Size = (int(Size_2, 16) * 2) + 2
            # print("ICON_LOCATION Size :", Size)
            sExtraData_Start_point += Size
            # print(sExtraData_Start_point)

        # find_MAC_Address_Point = sExtraData_Start_point

        find_extra_Size_1 = reverse_and_combine(hex_D[sExtraData_Start_point:sExtraData_Start_point + 4])
        find_extra_Size = int(find_extra_Size_1, 16)
        if find_extra_Size == 788:
            # print("Exist IconEnvironment(788)")
            sExtraData_Start_point += find_extra_Size
            # print(sExtraData_Start_point)

        find_extra_Size_2 = reverse_and_combine(hex_D[sExtraData_Start_point:sExtraData_Start_point + 4])
        find_extra_Size = int(find_extra_Size_2, 16)
        if find_extra_Size == 16:
            # print("Exist SpecialFolderDataBlock(16)")
            sExtraData_Start_point += find_extra_Size
            # print(sExtraData_Start_point)

        find_extra_Size_3 = reverse_and_combine(hex_D[sExtraData_Start_point:sExtraData_Start_point + 4])
        find_extra_Size = int(find_extra_Size_3, 16)
        if find_extra_Size == 28:
            # print("Exist KnownFolderDataBlock(28)")
            sExtraData_Start_point += find_extra_Size
            # print(sExtraData_Start_point)

        find_extra_Size_4 = reverse_and_combine(hex_D[sExtraData_Start_point:sExtraData_Start_point + 4])
        find_extra_Size = int(find_extra_Size_4, 16)
        if find_extra_Size == 96:
            NetBios_1 = hex_D[sExtraData_Start_point+16:sExtraData_Start_point+32]
            NetBios_2 = ''.join(NetBios_1)

            NetBios_2_1 = ''.join(
                [chr(int(''.join(c), 16)) for c in zip(NetBios_2[0::2], NetBios_2[1::2])])
            self.NetBios_3 = NetBios_2_1[:-1].replace("\0", "")
            #print("NetBios :", self.NetBios_3)

            MAC_ADD_Point = sExtraData_Start_point + 58
            self.MAC_ADD = ':'.join(hex_D[MAC_ADD_Point:MAC_ADD_Point + 6]).upper()
            #print("MAC_Address_Current :", self.MAC_ADD)

            MAC_ADD_Point = sExtraData_Start_point + 90
            self.MAC_ADD_2 = ':'.join(hex_D[MAC_ADD_Point:MAC_ADD_Point + 6]).upper()
            # print("MAC_Address_Birth :", MAC_ADD)

        wr.writerow([lnk_len, LinkFile_Name, self.File_Size, self.ctime, self.mtime, self.atime, self.Original_File_Name_1, self.LinkFile_Size_3,\
                     self.Creation_time_3, self.Write_time_3, self.Access_time_3, self.Drive_Type_3, self.Drive_Serial_Number_2, \
                     self.Local_Base_Path_3, self.MAC_ADD, self.MAC_ADD_2, self.NetBios_3, LinkFile])
        lnk_len += 1

def search(dirname):
    global lnk_len
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if (full_filename.find("$") == -1) and (ext == '.lnk'):
                    full_filename_2 = full_filename.replace("/", "\\")
                    filename = full_filename_2.split('\\')[-1]
                    try:
                        da = lnk_class()
                        da.lnk(full_filename_2, filename)
                    except:
                        pass
    except:
        pass

f = open('write.csv', 'w', -1, 'utf-8', newline='')
wr = csv.writer(f)
try:
    search("c:\\")
except:
    pass
f.close()