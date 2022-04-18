# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# GUI
import Message_Box.message_box as message_box

# Другое
import methods as Method

class QMessageBox(Method.CreateFormWindow):
	signalButton = QtCore.pyqtSignal(str)

	def __init__(self, text, button_1, button_2, parent=None):
		super().__init__(parent)
		self.ui = message_box.Ui_Form()
		self.ui.setupUi(self)

		# Создание всех нужных переменных
		_translate = QtCore.QCoreApplication.translate

		buttons_font = QtGui.QFont()
		buttons_font.setPointSize(11)
		buttons_font.setBold(True)
		buttons_font.setWeight(75)

		buttons_style = """
QPushButton{
	color: white;
	border-radius: 12px;
	background-color: #946FA6;
}

QPushButton:hover{
	background-color: #9A76AB;
}

QPushButton:pressed{
	background-color: #8E68A2;
}
"""

		self.ui.PlainTextEdit.setPlainText(text)
		if button_1 != None and button_2 != None:
			self.Button_1 = QtWidgets.QPushButton(self.ui.Window)
			self.Button_1.setGeometry(QtCore.QRect(20, 100, 161, 41))
			self.Button_1.setFont(buttons_font)
			self.Button_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			self.Button_1.setStyleSheet(buttons_style)

			self.Button_2 = QtWidgets.QPushButton(self.ui.Window)
			self.Button_2.setGeometry(QtCore.QRect(190, 100, 161, 41))
			self.Button_2.setFont(buttons_font)
			self.Button_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			self.Button_2.setStyleSheet(buttons_style)

			self.Button_1.setText(_translate('Form', button_1))
			self.Button_2.setText(_translate('Form', button_2))

			self.Button_1.clicked.connect(lambda: self.signalButton.emit(button_1))
			self.Button_2.clicked.connect(lambda: self.signalButton.emit(button_2))
		elif button_1 != None:
			self.Button_1 = QtWidgets.QPushButton(self.ui.Window)
			self.Button_1.setGeometry(QtCore.QRect(110, 100, 161, 41))
			self.Button_1.setFont(buttons_font)
			self.Button_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			self.Button_1.setStyleSheet(buttons_style)

			self.Button_1.setText(_translate('Form', button_1))
			self.Button_1.clicked.connect(lambda: self.signalButton.emit(button_1))
		elif button_2 != None:
			self.Button_2 = QtWidgets.QPushButton(self.ui.Window)
			self.Button_2.setGeometry(QtCore.QRect(110, 100, 161, 41))
			self.Button_2.setFont(buttons_font)
			self.Button_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			self.Button_2.setStyleSheet(buttons_style)

			self.Button_2.setText(_translate('Form', button_2))
			self.Button_2.clicked.connect(lambda: self.signalButton.emit(button_2))

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(lambda: self.close())
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

class MessageBox:
	def __init__(self, text='', button_1=None, button_2=None):
		self.message_box = QMessageBox(text, button_1, button_2)
		self.message_box.signalButton.connect(lambda: self.message_box.close())
		self.message_box.show()