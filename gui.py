# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'minecraft-instance-manager-qt.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 385)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.instances_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.instances_listWidget.setGeometry(QtCore.QRect(10, 40, 261, 241))
        self.instances_listWidget.setObjectName("instances_listWidget")
        self.storage_location_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.storage_location_lineEdit.setGeometry(QtCore.QRect(10, 320, 261, 21))
        self.storage_location_lineEdit.setObjectName("storage_location_lineEdit")
        self.active_instance_label = QtWidgets.QLabel(self.centralwidget)
        self.active_instance_label.setGeometry(QtCore.QRect(10, 10, 521, 21))
        self.active_instance_label.setObjectName("active_instance_label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 290, 531, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.storage_location_label = QtWidgets.QLabel(self.centralwidget)
        self.storage_location_label.setGeometry(QtCore.QRect(10, 300, 101, 21))
        self.storage_location_label.setObjectName("storage_location_label")
        self.browse_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.browse_pushButton.setGeometry(QtCore.QRect(290, 320, 111, 21))
        self.browse_pushButton.setObjectName("browse_pushButton")
        self.set_default_location_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.set_default_location_pushButton.setGeometry(QtCore.QRect(340, 350, 141, 21))
        self.set_default_location_pushButton.setObjectName("set_default_location_pushButton")
        self.storage_location_OK_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.storage_location_OK_pushButton.setGeometry(QtCore.QRect(420, 320, 111, 21))
        self.storage_location_OK_pushButton.setObjectName("storage_location_OK_pushButton")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(290, 40, 241, 231))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.rename_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.rename_pushButton.setObjectName("rename_pushButton")
        self.gridLayout.addWidget(self.rename_pushButton, 1, 1, 1, 1)
        self.delete_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.delete_pushButton.setObjectName("delete_pushButton")
        self.gridLayout.addWidget(self.delete_pushButton, 2, 0, 1, 1)
        self.duplicate_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.duplicate_pushButton.setObjectName("duplicate_pushButton")
        self.gridLayout.addWidget(self.duplicate_pushButton, 2, 1, 1, 1)
        self.select_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.select_pushButton.setObjectName("select_pushButton")
        self.gridLayout.addWidget(self.select_pushButton, 0, 0, 1, 1)
        self.unselect_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.unselect_pushButton.setObjectName("unselect_pushButton")
        self.gridLayout.addWidget(self.unselect_pushButton, 0, 1, 1, 1)
        self.create_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.create_pushButton.setObjectName("create_pushButton")
        self.gridLayout.addWidget(self.create_pushButton, 1, 0, 1, 1)
        self.reset_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.reset_pushButton.setObjectName("reset_pushButton")
        self.gridLayout.addWidget(self.reset_pushButton, 3, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Minecraft instance manager"))
        self.active_instance_label.setText(_translate("MainWindow", "Active instance: "))
        self.storage_location_label.setText(_translate("MainWindow", "Storage location:"))
        self.browse_pushButton.setText(_translate("MainWindow", "Browse"))
        self.set_default_location_pushButton.setText(_translate("MainWindow", "set default location"))
        self.storage_location_OK_pushButton.setText(_translate("MainWindow", "OK"))
        self.rename_pushButton.setText(_translate("MainWindow", "Rename"))
        self.delete_pushButton.setText(_translate("MainWindow", "Delete"))
        self.duplicate_pushButton.setText(_translate("MainWindow", "Duplicate"))
        self.select_pushButton.setText(_translate("MainWindow", "Select"))
        self.unselect_pushButton.setText(_translate("MainWindow", "Unselect"))
        self.create_pushButton.setText(_translate("MainWindow", "Create"))
        self.reset_pushButton.setText(_translate("MainWindow", "Reset"))