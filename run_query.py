import sqlite3

# Путь к вашей базе данных
db_path = 'D:/fdd/databaseSQL3/db.sqlite3'  # Замените на путь к вашей базе данных, если нужно

# Подключаемся к базе данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Удаляем дубликаты, оставляя только один экземпляр
cursor.execute('''
    DELETE FROM product_category
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM product_category
        GROUP BY value
    );
''')

# Сохраняем изменения
conn.commit()

# Проверяем, остались ли дубликаты
cursor.execute('''
    SELECT value, COUNT(*)
    FROM product_category
    GROUP BY value
    HAVING COUNT(*) > 1;
''')
duplicates_after = cursor.fetchall()

# Выводим результаты
if duplicates_after:
    print("Остались дубликаты:")
    for value, count in duplicates_after:
        print(f"Значение: {value}, Количество: {count}")
else:
    print("Дубликаты успешно удалены!")

# Закрываем соединение
conn.close()
