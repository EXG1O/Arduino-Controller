# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtWidgets

# GUI
import Main_Window.main_window as main_window
from user_command_window import UserCommandPanelWindow
from message_box import MessageBox

# Другое
from serial.tools import list_ports
import methods as Method
import webbrowser
import pyfirmata
import serial
import json
import time
import os

# Главное окно
class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = main_window.Ui_MainWindow()
		self.ui.setupUi(self)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		# Запуск всех нужных потоков
		self.update_ports_combobox_theard = UpdatePortsComboBox()
		self.update_ports_combobox_theard.signalUpdatePortsComboBox.connect(self.update_ports_combobox)
		self.update_ports_combobox_theard.start()

		self.update_user_commands_list_widget_theard = UpdateUserCommandsListWidget()
		self.update_user_commands_list_widget_theard.signalUpdateUserCommandsListWidget.connect(self.update_user_commands_list_widget)
		self.update_user_commands_list_widget_theard.start()

		# Оброботчик основных кнопок
		self.ui.AddNewUserCommandButton.clicked.connect(self.add_new_user_command_button)
		self.ui.EditUserCommandButton.clicked.connect(self.edit_user_command_button)
		self.ui.RemovUserCommandButton.clicked.connect(self.remove_user_commans_button)
		self.ui.OnOrOffProgramButton.clicked.connect(self.on_or_off_program_button)

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
	def get_select_item(func):
		def wrapper(self):
			select_item = self.ui.UserCommandsListWidget.selectedItems()
			if select_item != []:
				func(self, select_item[0])
			else:
				MessageBox(text = 'Вы не выбрали команду в списке команд, которую вы хотите редактировать!', button_1 = 'Щас исправлю...')
		return wrapper
	# ==================================================================

	# Логика для основных кнопок
	# ==================================================================
	def add_new_user_command_button(self):
		self.user_command_window = UserCommandPanelWindow(self.ui.AddNewUserCommandButton.text())
		self.user_command_window.show()

	@get_select_item
	def edit_user_command_button(self, select_item = None):
		self.edit_user_command_button = UserCommandPanelWindow(self.ui.EditUserCommandButton.text(), select_item[0])
		self.edit_user_command_button.show()

	@get_select_item
	def remove_user_commans_button(self, select_item = None):
		message_box = MessageBox(text  = f'Вы точно хотите удалить команду "{select_item[0].text()}"?', button_1 = 'Да', button_2 = 'Нет')
		message_box.message_box.signalButton.connect(lambda text: self.remove_user_command(message_box.message_box, text, select_item[0]))

	def on_or_off_program_button(self):
		on_or_off_program_button_text = self.ui.OnOrOffProgramButton.text()
		if  on_or_off_program_button_text == 'Включить программу':
			usb_port = self.ui.PortsListComboBox.currentText()
			if usb_port != '':
				self.on_program()
			else:
				MessageBox(text = 'Вы не выбрали USB порт из списка USB портов, к которому подключена ваша Arduino плата!', button_1 = 'Щас исправлю...')
		else:
			self.off_program()
	# ==================================================================

	# Обычные функции
	# ==================================================================
	def remove_user_command(self, message_box, user_answer, select_item):
		message_box.close()

		if user_answer == 'Да':
			user_command_name = select_item.text().split(': ')[0]
			user_commands = Method.get_user_commands()

			user_command_value = 0
			for user_command in user_commands:
				if user_command['Command_Name'] == user_command_name:
					break
				user_command_value += 1

			user_commands.pop(user_command_value - 1)
			with open('User-Commands.json', 'w') as file:
				file.write(json.dumps(user_commands, ensure_ascii = False, indent = 2))

			MessageBox(text = f'Вы успешно удалили команду "{user_command_name}".', button_1 = 'Окей')

	def on_program(self):
		self.ui.OnOrOffProgramButton.setText('Выключить программу')

		self.arduino_board = ArduinoBoard(self.ui.PortsListComboBox.currentText())
		self.arduino_board.start()

	def off_program(self):
		self.ui.OnOrOffProgramButton.setText('Включить программу')

		self.arduino_board.arduino_board_run = False
	# ==================================================================

	# Сигналы QtCore.pyqtSignal
	# ==================================================================
	def update_ports_combobox(self, usb_ports):
		self.ui.PortsListComboBox.clear()

		for port in usb_ports:
			port = str(port).split(' - ')[0]
			if port != 'COM1':
				self.ui.PortsListComboBox.addItem(port)

	def update_user_commands_list_widget(self, user_commands):
		self.ui.UserCommandsListWidget.clear()

		for user_command in user_commands:
			item = QtWidgets.QListWidgetItem()
			item.setTextAlignment(QtCore.Qt.AlignLeft)
			item.setText(f"Команда: {user_command['Command_Name']}")
			self.ui.UserCommandsListWidget.addItem(item)
	# ==================================================================

# Поток для обновления занчений в списке USB портов
class UpdatePortsComboBox(QtCore.QThread):
	signalUpdatePortsComboBox = QtCore.pyqtSignal(list)

	def __init__(self):
		QtCore.QThread.__init__(self)

	def run(self):
		old_usb_ports = list_ports.comports()
		self.signalUpdatePortsComboBox.emit(old_usb_ports)

		while True:
			new_usb_ports = list_ports.comports()
			if old_usb_ports != new_usb_ports:
				old_usb_ports = new_usb_ports
				self.signalUpdatePortsComboBox.emit(old_usb_ports)
			time.sleep(0.1)

# Поток для обновления занчений в таблицы пользовадских команд
class UpdateUserCommandsListWidget(QtCore.QThread):
	signalUpdateUserCommandsListWidget = QtCore.pyqtSignal(list)

	def __init__(self):
		QtCore.QThread.__init__(self)

	def run(self):
		user_commands = Method.get_user_commands()
		self.signalUpdateUserCommandsListWidget.emit(user_commands)

		while True:
			new_user_commands = Method.get_user_commands()
			if user_commands != new_user_commands:
				user_commands = new_user_commands
				self.signalUpdateUserCommandsListWidget.emit(user_commands)
			time.sleep(0.1)

# Поток для отслеживания событий Arduino платы
class ArduinoBoard(QtCore.QThread):
	signalOffProgram = QtCore.pyqtSignal()

	def __init__(self, usb_port):
		QtCore.QThread.__init__(self)

		self.usb_port = usb_port
		self.arduino_board_run = True

	def run(self):
		try:
			self.board = pyfirmata.Arduino(self.usb_port)
			it = pyfirmata.util.Iterator(self.board)
			it.start()
		except serial.serialutil.SerialException:
			self.signalOffProgram.emit()

		button_press = False
		while self.arduino_board_run:
			user_commands = Method.get_user_commands()
			for user_command in user_commands:
				board_port = int(user_command['Arduino_Port'].replace('D', '').strip())
				self.board.digital[board_port].mode = pyfirmata.INPUT
				value = self.board.digital[board_port].read()

				if value == True and button_press == False:
					button_press = True

					if os.path.isfile(f'\"{user_command["Command"]}\"'):
						os.system(f'\"{user_command["Command"]}\"')
					else:
						webbrowser.open(user_command['Command'])
				elif value == False and button_press == True:
					button_press = False