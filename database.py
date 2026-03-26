import sqlite3

def conectar():
    return sqlite3.connect('doacoes.db')


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantidade INTEGER NOT NULL
    )
    ''')

    conn.commit()
    conn.close()