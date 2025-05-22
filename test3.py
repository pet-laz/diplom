with open('diseases.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Обрабатываем строки
cleaned_lines = []
for line in lines:
    # Разделяем строку по ";" и обрезаем пробелы вокруг каждого элемента
    parts = [part.strip() for part in line.strip().split(';')]
    # Собираем строку обратно
    cleaned_line = ';'.join(parts)
    cleaned_lines.append(cleaned_line)

# Записываем очищенные строки в новый файл
with open('output.csv', 'w', encoding='utf-8') as file:
    for line in cleaned_lines:
        file.write(line + '\n')
