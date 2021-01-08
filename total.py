from tkinter import Tk
from tkinter import messagebox as msg
from PyQt5 import QtWidgets
from submain import Progress_Bar


class MainWindow(QtWidgets.QDialog, Progress_Bar):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def change(self):
        self.label.setText("수집 시작")
        self.label.update()
        self.CollectData(0)

    def CollectData(self, listcount):
        sdatt = str(listcount) + "개를 수집하였습니다."
        if (listcount != 0):
            root = Tk()
            root.withdraw()
            msg.showinfo("수집 완료", sdatt)

'''           
def Dialogs():
    import test
    Dialog = QtWidgets.QDialog()
    s = test.Ui_Dialog()
    s.setupUi(Dialog)
    Dialog.show()
'''
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    import test
    Dialog = QtWidgets.QDialog()
    s = test.Ui_Dialog()
    datat = s.setupUi(Dialog)

    mainWindow.close()
    mainWindow.CollectData(datat)
    Dialog.show()
    sys.exit(app.exec_())
