
import trivia
import imageCapture
import os
import sys
import time
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.runScriptButton = QtWidgets.QPushButton(self.centralwidget)
        self.runScriptButton.setGeometry(QtCore.QRect(40, 430, 351, 61))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.runScriptButton.setFont(font)
        self.runScriptButton.setObjectName("runScriptButton")
        self.screenshotButton = QtWidgets.QPushButton(self.centralwidget)
        self.screenshotButton.setGeometry(QtCore.QRect(420, 430, 351, 61))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.screenshotButton.setFont(font)
        self.screenshotButton.setObjectName("screenshotButton")
        self.resultsText = QtWidgets.QTextEdit(self.centralwidget)
        self.resultsText.setGeometry(QtCore.QRect(110, 70, 591, 321))
        self.resultsText.setReadOnly(False)
        self.resultsText.setObjectName("resultsText")
        font.setPointSize(23)
        self.resultsText.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        
        self.runScriptButton.clicked.connect(self.runScript)
        self.screenshotButton.clicked.connect(self.screenshot)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HQ Trivia Bot"))
        self.runScriptButton.setText(_translate("MainWindow", "Run script..."))
        self.screenshotButton.setText(_translate("MainWindow", "Screenshot"))

    def runScript(self):
        subprocess.Popen('python trivia.py')




    def screenshot(self):
        trivia.snapImage()
        time.sleep(5)
        with open(r'''C:\Users\mjoh0\Desktop\Projects\OCR\results.txt''', 'r') as fin:
            self.resultsText.setText(fin.read())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

