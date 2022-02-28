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