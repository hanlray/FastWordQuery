# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'updates.ui'
#
# Created: Sat Sep 10 10:16:01 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from aqt.qt import *

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_DialogUpdates(object):
    def setupUi(self, DialogUpdates):
        DialogUpdates.setObjectName(u"DialogUpdates")
        DialogUpdates.resize(500, 400)
        self.verticalLayout = QVBoxLayout(DialogUpdates)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelUpdates = QLabel(DialogUpdates)
        self.labelUpdates.setWordWrap(True)
        self.labelUpdates.setOpenExternalLinks(True)
        self.labelUpdates.setObjectName(u"labelUpdates")
        self.verticalLayout.addWidget(self.labelUpdates)
        self.textBrowser = QTextBrowser(DialogUpdates)
        self.textBrowser.setObjectName(u"textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        #spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #self.horizontalLayout.addItem(spacerItem)
        #self.always = QPushButton(DialogUpdates)
        #self.always.setObjectName(u"always"))
        #self.horizontalLayout.addWidget(self.always)
        self.update = QPushButton(DialogUpdates)
        self.update.setObjectName(u"update")
        self.horizontalLayout.addWidget(self.update, 0, Qt.AlignCenter)
        #self.dont = QPushButton(DialogUpdates)
        #self.dont.setObjectName(u"dont"))
        #self.horizontalLayout.addWidget(self.dont)
        #self.never = QPushButton(DialogUpdates)
        #self.never.setObjectName(u"never"))
        #self.horizontalLayout.addWidget(self.never)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DialogUpdates)
        QMetaObject.connectSlotsByName(DialogUpdates)

    def retranslateUi(self, DialogUpdates):
        DialogUpdates.setWindowTitle(_translate("DialogUpdates", "FastWQ - Update Checker", None))
        self.labelUpdates.setText(_translate("DialogUpdates", "<html><head/><body><p>A new version of {0} is available for download! </p><p>Do you want to update {1}to version {2}?</p><p>Changes from your version are listed below:</p></body></html>", None))
        #self.always.setText(_translate("DialogUpdates", "Always update", None))
        self.update.setText(_translate("DialogUpdates", "Update", None))
        #self.dont.setText(_translate("DialogUpdates", "Don\'t update", None))
        #self.never.setText(_translate("DialogUpdates", "Never", None))

