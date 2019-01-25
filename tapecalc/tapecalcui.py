# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tapecalc.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(421, 442)
        self.cmbArtist = QtWidgets.QComboBox(Dialog)
        self.cmbArtist.setGeometry(QtCore.QRect(80, 10, 331, 22))
        self.cmbArtist.setObjectName("cmbArtist")
        self.cmbAlbum = QtWidgets.QComboBox(Dialog)
        self.cmbAlbum.setGeometry(QtCore.QRect(80, 40, 331, 22))
        self.cmbAlbum.setObjectName("cmbAlbum")
        self.cmbLength = QtWidgets.QComboBox(Dialog)
        self.cmbLength.setGeometry(QtCore.QRect(80, 70, 91, 22))
        self.cmbLength.setCurrentText("")
        self.cmbLength.setObjectName("cmbLength")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 47, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 61, 21))
        self.label_3.setObjectName("label_3")
        self.txtOutput = QtWidgets.QTextEdit(Dialog)
        self.txtOutput.setGeometry(QtCore.QRect(10, 130, 401, 301))
        self.txtOutput.setObjectName("txtOutput")
        self.evenSides = QtWidgets.QCheckBox(Dialog)
        self.evenSides.setGeometry(QtCore.QRect(80, 100, 131, 17))
        self.evenSides.setObjectName("evenSides")
        self.cmbExtra = QtWidgets.QComboBox(Dialog)
        self.cmbExtra.setGeometry(QtCore.QRect(240, 70, 91, 22))
        self.cmbExtra.setObjectName("cmbExtra")
        self.chkAllowBonus = QtWidgets.QCheckBox(Dialog)
        self.chkAllowBonus.setGeometry(QtCore.QRect(200, 100, 211, 17))
        self.chkAllowBonus.setObjectName("chkAllowBonus")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(190, 70, 31, 20))
        self.label_4.setObjectName("label_4")
        self.cmdComplete = QtWidgets.QPushButton(Dialog)
        self.cmdComplete.setGeometry(QtCore.QRect(340, 70, 71, 51))
        self.cmdComplete.setObjectName("cmdComplete")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "TapeCalc"))
        self.label.setText(_translate("Dialog", "Artist"))
        self.label_2.setText(_translate("Dialog", "Album"))
        self.label_3.setText(_translate("Dialog", "Side Length"))
        self.evenSides.setText(_translate("Dialog", "Aim for even sides"))
        self.chkAllowBonus.setText(_translate("Dialog", "Include Bonus Tracks"))
        self.label_4.setText(_translate("Dialog", "Extra"))
        self.cmdComplete.setText(_translate("Dialog", "Recording\n"
"Complete"))

