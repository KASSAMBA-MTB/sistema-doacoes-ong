import sqlite3
from werkzeug.security import generate_password_hash


# 🔌 Conexão com banco
def conectar():
    return sqlite3.connect("doacoes.db")


# 📦 TABELA DE DOAÇÕES
def criar_tabela_doacoes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# 👤 TABELA DE USUÁRIOS
def criar_tabela_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# 🔐 USUÁRIO PADRÃO (COM SENHA SEGURA)
def criar_usuario_padrao():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", ('admin',))
    usuario = cursor.fetchone()

    if not usuario:
        senha_hash = generate_password_hash("123")

        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            ('admin', senha_hash)
        )

        print("✅ Usuário admin criado com sucesso!")

    conn.commit()
    conn.close()