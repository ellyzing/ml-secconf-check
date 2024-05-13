import csv

# Открываем CSV файл для чтения
with open('parsed_lines.csv', 'r') as file:
    lines = file.readlines()

# Проходимся по каждой строке и меняем значение последнего столбца
for i in range(1, len(lines)):
    values = lines[i].split(';')
    last_value = values[-1].strip()
    if last_value == '0':
        values[-1] = '1'
    elif last_value == '1':
        values[-1] = '0'
    lines[i] = ';'.join(values) + '\n'

# Записываем измененные данные обратно в CSV файл
with open('output1.csv', 'w') as file:
    file.writelines(lines)
