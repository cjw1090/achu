# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LinkFile.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, tab,tapname_list):

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

        self.Recently_Detail = QtWidgets.QTableWidget(tab)
        self.Recently_Detail.setObjectName("Recently_Detail")
        self.gridLayout_5.addWidget(self.Recently_Detail, 0, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.Recently_Detail.setFont(font)
        self.Recently_Detail.setMouseTracking(False)
        self.Recently_Detail.setTabletTracking(False)
        self.Recently_Detail.setAcceptDrops(False)
        self.Recently_Detail.setToolTipDuration(-1)
        self.Recently_Detail.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Recently_Detail.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Recently_Detail.setAutoScroll(True)
        self.Recently_Detail.setAutoScrollMargin(16)
        self.Recently_Detail.setSortingEnabled(True)
        self.Recently_Detail.setShowGrid(True)
        self.Recently_Detail.setRowCount(0)
        self.Recently_Detail.setColumnCount(5)
        self.Recently_Detail.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.Recently_Detail.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.Recently_Detail.setHorizontalHeaderItem(0, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.Recently_Detail.setHorizontalHeaderItem(1, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.Recently_Detail.setHorizontalHeaderItem(2, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.Recently_Detail.setHorizontalHeaderItem(3, item)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
        item.setFont(font)
        self.Recently_Detail.setHorizontalHeaderItem(3, item)

        self.Recently_Detail.setHorizontalHeaderLabels(["File Name", "Create Time", "Modified Time", "Run Time", "Run Count"])
        tapname_list.append(self.Recently_Detail.objectName())
        header = self.Recently_Detail.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for i in range(1, self.Recently_Detail.columnCount() - 1):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
    def rowCount(self,number):
        self.Recently_Detail.setRowCount(number)

    def update(self):
        self.Recently_Detail.update()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
