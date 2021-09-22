import zipfile, os, time, sys

class VShell(object):#класс эмулятора командной строки

	__path = []#текущее местоположение в файловой системе сохраняется в список path

	def __init__(self):
		self.__file_system_name = self.__get_file_system_name()#получаем имя архива
		if (self.is_successful_start()):
			self.__file_system = zipfile.ZipFile(self.__file_system_name, 'r')#открываем для работы zip архив
			self.__root_dir = self.__file_system_name[:self.__file_system_name.index('.')]#забираем имя корневой директории
			self.__append_dir(self.__root_dir)

	def is_successful_start(self):
		return self.__success_input

	def __get_file_system_name(self):#приватный метод для получения имени архива
		self.__success_input = False#переменная для проверки корректности ввода
		zip_name = ""
		if (len(sys.argv) > 1):#если осуществлен ввод более двух слов, то из argv мы можем взять 1-ый элемент
				zip_name = sys.argv[1]#ввод имени архива как аргумента командной строки
		if (zipfile.is_zipfile(zip_name)):#проверка на существование архива
			self.__success_input = True
		else:
			print("zip file '" + zip_name + "' does not exists")
			zip_name = "does_not_exists"
		return zip_name#если архив существует, то будет возвращено его имя

	def __append_dir(self, dir_name):
		self.__path.append(dir_name)

	def __delete_dir(self):
		if (len(self.__path) > 1):#чтобы случайно не удалить имя корневой директории
			self.__path.pop()

	def print_cmd(self):
		print(self.get_working_dir() + "> ", end='')

	def get_working_dir(self):#возвразает текущую рабочую папку от самого корня
		answer = ""
		for directory in self.__path:
			answer += directory + "/"
		return answer

	def __is_path_from_current(self, path):#проверка на существование директории по текущему пути
		#на вход поступает строка - путь, он обязательно должен начинаться с косой черты
		file_system_tree = self.__file_system.namelist()
		abs_path = self.get_working_dir() + path[1:] + '/'#создается полный путь к папке от текущей директории и проверяется его наличие в zip архиве
		for p in file_system_tree:#если с помощью cd ввести ../text.txt, то директория не будет найдена, тк это попытка открыть текстовый файл как директорию
		#в переменнной abs_path это будет выглядеть так: ../text.txt/ 
			if (p == abs_path):#второе условие: если путь задан абсолютно от корневой папки
				return True
		return False

	def __is_path_from_root(self, path):#проверка на существование директории по абсолютному пути 
		#на вход поступает строка - путь, он обязательно должен начинаться с косой черты
		file_system_tree = self.__file_system.namelist()
		for p in file_system_tree:
			if (p == self.__root_dir + path + '/'):#если путь задан абсолютно от корневой папки
				return True
		return False

	def __is_file(self, file_name):#проверка файла на существование
		file_system_tree = self.__file_system.namelist()
		for p in file_system_tree:
			if (p == self.get_working_dir() + file_name ):
				return True
		return False

	def change_dir(self, path):
		if (path == "-"):#если введен символ "-", то подняться на одну папку
			self.__delete_dir()
		elif (path == ".." or path == ""):#если введены две точки ".." или ничего, то подняться в корневой каталог
			while (len(self.__path) != 1):
				self.__delete_dir()
		else:#иначе перейти в каталог, если он существует, или вывести сообщение, что такого каталога нет
			if (self.__is_path_from_current(path)):
				path_list = path.split('/')#разбиваем директории на отдельные элементы
				for p in path_list:
					if (len(p) != 0):
						self.__append_dir(p)#добавляем директории попорядку в текущий путь
			elif (self.__is_path_from_root(path)):
				path_list = path.split('/')#разбиваем директории на отдельные элементы 
				while (len(self.__path) != 1):#чистим весь путь до корня
					self.__delete_dir()
				for p in path_list:
					if (len(p) != 0):
						self.__append_dir(p)#добавляем директории попорядку в текущий путь
			else:
				print("the dir '" + path + "' does not exists")

	def close(self):
		self.__file_system.close()

	def get_dir_files_info(self, arg=""):#реализация команды ls
		answer = []#ответ - информация о файлах
		if (arg == "-l"):#сли введен ключ -l, то необходимо вывести подробную информацию о файлах (дата редактирования, размер в байтах) и директориях
			dir_info = os.listdir(self.get_working_dir()[:len(self.get_working_dir()) - 1])#метод модуля os.path, дающий инфорацию о директрии
			for item in dir_info:
				file_size = ""#размер файла, вынесено отдельно, тк при попытке узнать размер директории будет ошибка, тк директория - не файл
				if (self.__is_file(item)):#если перед нами файл
					file_size = self.__file_system.getinfo(self.get_working_dir() + item).file_size#и мы можем определить его размер
				answer.append([item, time.ctime(os.path.getmtime(self.get_working_dir() + item)), file_size])
		elif (arg == ""):#если нет аргумента -l, то должны вывестись только имена файлов
			answer = os.listdir(self.get_working_dir()[:len(self.get_working_dir()) - 1])
		return answer

	def print_file_info(self, dir_files_info):
		if (len(dir_files_info) != 0):#если в dir_files_info есть элементыы, то метод выполняется
			if (isinstance(dir_files_info[0], str)):#если нулевой объект имеет строковый тип, то команда ls была введена без ключа -l
				for file in dir_files_info:
					print(file, end = '   ')#требуется просто вывести имена файлов
				print()
			else:
				col_width = max(len(str(info)) for vector in dir_files_info for info in vector) + 2  #определение длины самой длиной строки для красивого отображения по столбцам
				for file_info in dir_files_info:
				    print("".join(str(info).ljust(col_width) for info in file_info))

	def get_file_text(self, file_name = ""):
		if (self.__is_file(file_name)):
			return self.__file_system.read(self.get_working_dir() + file_name).decode('utf-8', errors="replace")
		else:
			return "does_not_exists"

def get_cmd_list(inp):
	inp = inp.split(';')#разбивка на команды
	inp = [item for item in inp if (item != '')]#очитска от возможных пустых элементов
	cmd_list = []#ответ - список команд с аргументами
	for item in inp:
		cmd_list.append(item.split())
	cmd_list = [cmd for cmd in cmd_list if (len(cmd) != 0)]#если будут пустые элементы, то их необходимо удалить
	return cmd_list



def main():
	vshell = VShell()
	if (vshell.is_successful_start()):#Если запускается из командной строки и имя архива введено правильно, то начинается работа программы
		cmd = ""#название команды
		arg = ""#аргумент для команды
		cmd_list = []#конвеер команд
		while True:
			if (len(cmd_list) == 0):#если список команд пуст, то необходимо ввести новые команды
				vshell.print_cmd()#печать ввода
				inp = input()#получение команд
				cmd_list = get_cmd_list(inp)#запись команд в список
			if (len(cmd_list[0]) > 1):#в списке команд заведомо не лежат пустые элементы, поэтому там может быть 1 и больше элементов
				cmd = cmd_list[0][0]#сначала идет команда
				arg = cmd_list[0][1]#потом идет ее аргумент
			else:#если длина равна 1, то задана только команда, без параметров
				cmd = cmd_list[0][0]
			if (cmd == "exit"):
				vshell.close()
				break
			elif (cmd == "cd"):
				vshell.change_dir(arg)#у cd аргумент - путь к директории
			elif (cmd == "pwd"):
				print(vshell.get_working_dir())
			elif (cmd == "ls"):
				vshell.print_file_info(vshell.get_dir_files_info(arg))#у ls аргумент -l - подробная информация
			elif (cmd == "cat"):
				if (vshell.get_file_text(arg) != "does_not_exists"):
					print(vshell.get_file_text(arg))
				else:
					print("cannot open '" + arg +  "': No such file or directory")
			else:
				print("command '" + cmd + "' is not found")
			cmd = ""#очищаем переменную команды для дальнейшего использования
			arg = ""#очищаем аргумент
			if (len(cmd_list) != 0):#удаляем из списка текущие команду и аргумент
				cmd_list.pop(0)

if __name__ == "__main__":
	main()
	
