# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtWidgets

# GUI
from main_window import MainWindow

# Другое
import methods as Method
import json
import sys

# Создание всех нужных файлов
# ==================================================================
if Method.find_file('User-Commands.json') == False:
	with open('User-Commands.json', 'a') as file:
		file.write(json.dumps([], ensure_ascii=False, indent=2))
# ==================================================================

# Запуск программы
# ==================================================================
if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	myapp = MainWindow()
	myapp.show()
	sys.exit(app.exec_())
# ==================================================================