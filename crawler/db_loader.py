"""
Импорт данных из CSV в SQLite базу данных с полнотекстовым индексом (FTS5).
После импорта можно выполнять быстрый поиск по содержимому файлов.
"""

import sqlite3
import csv
import os

CSV_FILE = './output/file_index.csv'
DB_FILE = './output/database.sqlite'

def create_db_and_import():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Создаём таблицу с полнотекстовым поиском (FTS5)
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS documents USING fts5(
            file_path, content
        )
    ''')

    # Читаем CSV и вставляем данные
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # пропустить заголовок
        rows = list(reader)

    cursor.executemany('INSERT INTO documents (file_path, content) VALUES (?, ?)', rows)
    conn.commit()

    # Проверка количества записей
    cursor.execute('SELECT COUNT(*) FROM documents')
    count = cursor.fetchone()[0]
    print(f"Импортировано {count} записей в таблицу 'documents'.")

    # Пример поиска
    search_term = input("Введите слово для поиска (или Enter для пропуска): ").strip()
    if search_term:
        cursor.execute("SELECT file_path, snippet(documents, 1, '<b>', '</b>', '...', 20) FROM documents WHERE content MATCH ? LIMIT 10", (search_term,))
        results = cursor.fetchall()
        if results:
            print(f"\nРезультаты поиска по '{search_term}':")
            for path, snippet in results:
                print(f"\nФайл: {path}\nОтрывок: {snippet}\n")
        else:
            print("Ничего не найдено.")

    conn.close()

if __name__ == '__main__':
    if not os.path.exists(CSV_FILE):
        print(f"Файл {CSV_FILE} не найден. Сначала запустите crawler.py")
    else:
        create_db_and_import()