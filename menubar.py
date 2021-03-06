# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tool.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import D_check
import test
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, qApp, QMenu, QMenuBar, QVBoxLayout, QMessageBox
class Ui_Dialog(object):
    def setupUi(self, Dialog):

        def hello(self):
            print("hello")

        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(1280, 840)

        exitAction = QAction(QIcon('exit.png'), 'Exit', parent=Dialog)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        SaveAction = QAction(QIcon('save.png'), 'Save', parent=Dialog)
        SaveAction.setShortcut('Ctrl+S')
        SaveAction.setStatusTip('Save')
        SaveAction.triggered.connect(hello)

        Anti_Action = QAction(QIcon('Anti.png'), 'Anti-Forensic Tool Execution Trace', parent=Dialog)
        Anti_Action.setStatusTip('Anti-Forensic Tool Execution Trace')
        Anti_Action.triggered.connect(hello)

        Mal_Action = QAction(QIcon('mal.png'), 'Malicious File Execution Trace', parent=Dialog)
        Mal_Action.setStatusTip('Malicious File Execution Trace')
        Mal_Action.triggered.connect(hello)

        Freq_Action = QAction(QIcon('freq.png'), 'Freqently Used File Trace', parent=Dialog)
        Freq_Action.setStatusTip('Freqently Used File Trace')
        Freq_Action.triggered.connect(hello)

        Cont_Action= QAction(QIcon('cont.png'), 'Continuous File Execution Trace', parent=Dialog)
        Cont_Action.setStatusTip('Continuous File Execution Trace')
        Cont_Action.triggered.connect(hello)

        Dele_Action = QAction(QIcon('dele.png'), 'Currently Deleted Executable Trace', parent=Dialog)
        Dele_Action.setStatusTip('Currently Deleted Executable Trace')
        Dele_Action.triggered.connect(Defile)

        self.menubar = QMenuBar(Dialog)
        self.menubar.setNativeMenuBar(False)
        self.filemenu = self.menubar.addMenu('&File')
        self.filemenu.addAction(exitAction)
        self.filemenu.addAction(SaveAction)
        self.toolmenu = self.menubar.addMenu('&Tool')
        self.toolmenu.addAction(Anti_Action)
        self.toolmenu.addAction(Freq_Action)
        self.toolmenu.addAction(Cont_Action)
        self.toolmenu.addAction(Dele_Action)
        self.toolmenu.addAction(Mal_Action)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
