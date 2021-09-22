# Bash-emulator
VShell - написанная на python программа, эмулирующая работу сеанса bash в Linux.
Использовались библиотеки:
1. zipfile - основная библиотека, которая использовалась при работе с архивом
2. os - использовалась для получения времени последней модификации файла
3. time - при выводе подробной информации о файле метод ctime позволял в читаемом виде отобразить информацию о последней модификации файла

Программа поддерживает команды pwd, cd (путь к файлу), ls (никакого аргумента или -l), cat (имя файла) с одним аргументом (написаны в скобках); поддерживается ввод команд в одну строку с разделителем ';'.
Программа запускается через командную строку - на вход поступает аргумент - имя ядра файловой системы (архива, который ее имитирует). Работа ведется в нераспакованном архиве. Далее создается объект класса VShell, запускается бесконечный цикл, в котором обрабатываются команды пользователя; команды кладутся в список и последовательно извлекаются в процессе выполнения.

