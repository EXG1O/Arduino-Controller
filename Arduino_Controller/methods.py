# PyQt5
from PyQt5 import QtCore, QtWidgets

# Другое
import json
import os

# Метод для получения пользовадских команд
def get_user_commands():
	with open('User-Commands.json', 'r') as file:
		user_commands = file.read()
		user_commands = json.loads(user_commands)
	return user_commands

# Метод для поиска файла
def find_file(file_name):
	find_file = False
	for file in os.listdir():
		if file == file_name:
			find_file = True
			break
	return find_file

# Класс для создания основы для MainWindow
class CreateMainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self, parent)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

	# Перетаскивание безрамочного окна
	# ==================================================================
	def center(self):
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def mousePressEvent(self, event):
		self.oldPos = event.globalPos()

	def mouseMoveEvent(self, event):
		try:
			delta = QtCore.QPoint(event.globalPos() - self.oldPos)
			self.move(self.x() + delta.x(), self.y() + delta.y())
			self.oldPos = event.globalPos()
		except AttributeError:
			pass

# Класс для создания основы для FormWindow
class CreateFormWindow(QtWidgets.QMainWindow):
	def __init__(self, parent):
		super().__init__(parent, QtCore.Qt.Window)
		self.setWindowModality(2)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

	# Перетаскивание безрамочного окна
	# ==================================================================
	def center(self):
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def mousePressEvent(self, event):
		self.oldPos = event.globalPos()

	def mouseMoveEvent(self, event):
		try:
			delta = QtCore.QPoint(event.globalPos() - self.oldPos)
			self.move(self.x() + delta.x(), self.y() + delta.y())
			self.oldPos = event.globalPos()
		except AttributeError:
			pass