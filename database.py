import sqlite3

def conectar():
    return sqlite3.connect('doacoes.db')


# 📦 TABELA DE DOAÇÕES
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


# 👤 TABELA DE USUÁRIOS
def criar_tabela_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        senha TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


# 🔐 USUÁRIO PADRÃO
def criar_usuario_padrao():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", ('admin',))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            ('admin', '123')
        )

    conn.commit()
    conn.close()