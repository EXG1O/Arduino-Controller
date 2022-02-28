# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtWidgets

# GUI
import Main_Window.User_Command_Window.user_command_window as user_command_window
from message_box import MessageBox

# Другое
import methods as Method
import json

# Окно для пользовадский команд
class UserCommandPanelWindow(QtWidgets.QMainWindow):
	def __init__(self, button_text, item = None, parent = None):
		super().__init__(parent, QtCore.Qt.Window)
		self.ui = user_command_window.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowModality(2)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		# Все нужные переменные
		self.button_text = button_text
		self.user_commands = Method.get_user_commands()

		# Обработчик основной кнопки
		self.ui.Button.setText(self.button_text)
		self.ui.Button.clicked.connect(self.button_button)

		if self.button_text == 'Редактировать команду':
			self.item = item

			old_user_command = self.item.text().replace('Команда: ', '').strip()

			self.user_command_value = 0
			for user_command in self.user_commands:
				if user_command['Command_Name'] == old_user_command:
					break
				self.user_command_value += 1

			self.ui.CommandNameLineEdit.setText(self.user_commands[self.user_command_value]['Command_Name'])
			self.ui.CommandLineEdit.setText(self.user_commands[self.user_command_value]['Command'])
			self.ui.ArduinoPortsListComboBox.setCurrentText(self.user_commands[self.user_command_value]['Arduino_Port'])

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(lambda: self.close())
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

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
	# ==================================================================

	# Декораторы
	# ==================================================================
	def check_user_command(func):
		def wrapper(self, message_box, user_answer):
			message_box.close()

			if user_answer == 'Да':
				command_name = self.ui.CommandNameLineEdit.text()
				command = self.ui.CommandNameLineEdit.text()

				if command_name == '':
					MessageBox(text = f'Вы не придумали имя команде!', button_1 = 'Щас исправлю...')
				elif command == '':
					MessageBox(text = f'Вы не указали, что должна делать данная команда!', button_1 = 'Щас исправлю...')
				else:
					find_user_command_name = False
					for user_command in self.user_commands:
						if user_command['Command_Name'] == command_name:
							find_user_command_name = True
							break

					if find_user_command_name == False or find_user_command_name == True and self.button_text == 'Редактировать команду' and self.user_commands[self.user_command_value]['Command_Name'] == command_name:
						func(self, message_box, user_answer)
					else:
						MessageBox(text = f'Команда с именем "{command_name}" уже существует!', button_1 = 'Щас исправлю...')
		return wrapper
	# ==================================================================

	# Логика основной кнопки
	# ==================================================================
	def button_button(self):
		if self.button_text == 'Добавить команду':
			message_box = MessageBox(text = 'Вы точно хотите добавить новую команду?', button_1 = 'Да', button_2 = 'Нет')
			message_box.message_box.signalButton.connect(lambda text: self.add_new_user_command(message_box.message_box, text))
		elif self.button_text == 'Редактировать команду':
			message_box = MessageBox(text = f'Вы точно хотите редактировать данную команду?', button_1 = 'Да', button_2 = 'Нет')
			message_box.message_box.signalButton.connect(lambda text: self.edit_user_command(message_box.message_box, text))
	# ==================================================================

	# Обычные функции
	# ==================================================================
	@check_user_command
	def add_new_user_command(self, message_box, user_answer):
		self.user_commands.append(
			{
				'Command_Name': self.ui.CommandNameLineEdit.text(),
				'Command': self.ui.CommandLineEdit.text(),
				'Arduino_Port': self.ui.ArduinoPortsListComboBox.currentText()
			}
		)
		with open('User-Commands.json', 'w') as file:
			file.write(json.dumps(self.user_commands, ensure_ascii = False, indent = 2))

		self.close()
		MessageBox(text = 'Вы успешно добавили новую команду.', button_1 = 'Окей')

	@check_user_command
	def edit_user_command(self, message_box, user_answer):
		self.user_commands[self.user_command_value].update(
			{
				'Command_Name': self.ui.CommandNameLineEdit.text(),
				'Command': self.ui.CommandLineEdit.text(),
				'Arduino_Port': self.ui.ArduinoPortsListComboBox.currentText()
			}
		)
		with open('User-Commands.json', 'w') as file:
			file.write(json.dumps(self.user_commands, ensure_ascii = False, indent = 2))

		self.close()
		MessageBox(text = 'Вы успешно редактировали команду.', button_1 = 'Окей')
	# ==================================================================