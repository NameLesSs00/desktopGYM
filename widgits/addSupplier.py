# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addSupplier.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(375, 391)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 42))
        self.widget.setStyleSheet(u"background-color:rgb(242, 198, 198);\n"
"border-radius:20px;")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color:rgb(0, 0, 0)")

        self.horizontalLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout.addWidget(self.widget)

        self.widget_5 = QWidget(Dialog)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setMinimumSize(QSize(100, 60))
        self.widget_5.setStyleSheet(u"#widget_5{\n"
"background-color:rgb(225, 218, 218);\n"
"border-radius:30px;\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.widget_5)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, -1, 6, 6)
        self.widget_6 = QWidget(self.widget_5)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setStyleSheet(u"")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.widget_6)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"color:rgb(0, 0, 0)")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.widget_6)

        self.widget_7 = QWidget(self.widget_5)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setStyleSheet(u"background-color:rgb(239, 239, 239);\n"
"border-radius:15px;")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_2 = QLineEdit(self.widget_7)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(0, 46))
        self.lineEdit_2.setStyleSheet(u"color:rgb(0, 0, 0)")
        self.lineEdit_2.setFrame(False)

        self.horizontalLayout_5.addWidget(self.lineEdit_2)


        self.verticalLayout_2.addWidget(self.widget_7)


        self.verticalLayout.addWidget(self.widget_5)

        self.widget_8 = QWidget(Dialog)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setMinimumSize(QSize(100, 60))
        self.widget_8.setStyleSheet(u"#widget_8{\n"
"background-color:rgb(225, 218, 218);\n"
"border-radius:30px;\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.widget_8)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(6, -1, 6, 6)
        self.widget_9 = QWidget(self.widget_8)
        self.widget_9.setObjectName(u"widget_9")
        self.widget_9.setStyleSheet(u"")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.widget_9)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"color:rgb(0, 0, 0)")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addWidget(self.widget_9)

        self.widget_10 = QWidget(self.widget_8)
        self.widget_10.setObjectName(u"widget_10")
        self.widget_10.setStyleSheet(u"background-color:rgb(239, 239, 239);\n"
"border-radius:15px;")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_3 = QLineEdit(self.widget_10)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMinimumSize(QSize(0, 46))
        self.lineEdit_3.setStyleSheet(u"color:rgb(0, 0, 0)")
        self.lineEdit_3.setFrame(False)

        self.horizontalLayout_7.addWidget(self.lineEdit_3)


        self.verticalLayout_3.addWidget(self.widget_10)


        self.verticalLayout.addWidget(self.widget_8)

        self.widget_11 = QWidget(Dialog)
        self.widget_11.setObjectName(u"widget_11")
        self.widget_11.setMinimumSize(QSize(100, 60))
        self.widget_11.setStyleSheet(u"#widget_11{\n"
"background-color:rgb(225, 218, 218);\n"
"border-radius:30px;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.widget_11)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(6, -1, 6, 6)
        self.widget_12 = QWidget(self.widget_11)
        self.widget_12.setObjectName(u"widget_12")
        self.widget_12.setStyleSheet(u"")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_12)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.widget_12)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"color:rgb(0, 0, 0)")

        self.horizontalLayout_8.addWidget(self.label_5)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)


        self.verticalLayout_4.addWidget(self.widget_12)

        self.widget_13 = QWidget(self.widget_11)
        self.widget_13.setObjectName(u"widget_13")
        self.widget_13.setStyleSheet(u"background-color:rgb(239, 239, 239);\n"
"border-radius:15px;")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_13)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_4 = QLineEdit(self.widget_13)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMinimumSize(QSize(0, 46))
        self.lineEdit_4.setStyleSheet(u"color:rgb(0, 0, 0)")
        self.lineEdit_4.setFrame(False)

        self.horizontalLayout_9.addWidget(self.lineEdit_4)


        self.verticalLayout_4.addWidget(self.widget_13)


        self.verticalLayout.addWidget(self.widget_11)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_4 = QPushButton(Dialog)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setMinimumSize(QSize(0, 50))
        self.pushButton_4.setStyleSheet(u"QPushButton {\n"
"    background-color: #FC4A4A;    /* bright red */\n"
"    color: white;\n"
"    border: none;                 /* remove default border */\n"
"    border-radius: 20px;          /* smooth rounded corners */\n"
"    font-weight: bold;\n"
"    font-size: 16px;\n"
"    padding: 10px 20px;\n"
"}\n"
"\n"
"/* Hover effect: slightly darker red */\n"
"QPushButton:hover {\n"
"    background-color: #E03B3B;\n"
"}\n"
"\n"
"/* Pressed effect: even darker red */\n"
"QPushButton:pressed {\n"
"    background-color: #C13030;\n"
"    padding-left: 18px;   /* subtle \"press\" effect */\n"
"    padding-top: 12px;\n"
"}\n"
"")

        self.horizontalLayout_2.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(Dialog)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setMinimumSize(QSize(0, 50))
        self.pushButton_5.setStyleSheet(u"QPushButton {\n"
"    background-color: #5AB62C;    /* base green */\n"
"    color: white;\n"
"    border: none;                 /* remove default border */\n"
"    border-radius: 20px;          /* smooth rounded corners */\n"
"    font-weight: bold;\n"
"    font-size: 16px;\n"
"    padding: 10px 20px;           /* vertical and horizontal padding */\n"
"}\n"
"\n"
"/* Hover animation effect */\n"
"QPushButton:hover {\n"
"    background-color: #4A9C26;   /* slightly darker green */\n"
"}\n"
"\n"
"/* Pressed (click) animation */\n"
"QPushButton:pressed {\n"
"    background-color: #3D7F20;   /* even darker green */\n"
"    padding-left: 18px;           /* subtle \"press\" effect */\n"
"    padding-top: 12px;\n"
"}\n"
"")

        self.horizontalLayout_2.addWidget(self.pushButton_5)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"New Supplier ", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Supplier\u2019s name:", None))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("Dialog", u"Enter the Supplier\u2019s name ", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Supplier\u2019s phone:", None))
        self.lineEdit_3.setText("")
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("Dialog", u"Enter the Supplier\u2019s phone ", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Supplier\u2019s Email:", None))
        self.lineEdit_4.setText("")
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("Dialog", u"Enter the Supplier\u2019s Email ", None))
        self.pushButton_4.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushButton_5.setText(QCoreApplication.translate("Dialog", u"Done", None))
    # retranslateUi

