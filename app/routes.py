from flask import Blueprint, render_template, request, redirect, flash, session
from database import conectar

# 🔥 PRIMEIRO: cria o blueprint
main = Blueprint('main', __name__)


# 🔐 LOGIN
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario == 'admin' and senha == '123':
            session['usuario'] = usuario
            flash('Login realizado com sucesso!')
            return redirect('/doar')
        else:
            flash('Usuário ou senha inválidos')

    return render_template('login.html')


# 🔓 LOGOUT
@main.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Logout realizado com sucesso!')
    return redirect('/login')


# 🏠 HOME
@main.route('/')
def home():
    return redirect('/login')


# 📦 DOAÇÕES
@main.route('/doar', methods=['GET', 'POST'])
def doar():
    if 'usuario' not in session:
        return redirect('/login')

    if request.method == 'POST':
        item = request.form.get('item')
        quantidade = request.form.get('quantidade')

        if item and quantidade:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO doacoes (item, quantidade) VALUES (?, ?)",
                (item, quantidade)
            )

            conn.commit()
            conn.close()

            flash('Doação cadastrada com sucesso!')

        return redirect('/doar')

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, item, quantidade FROM doacoes")
    doacoes = cursor.fetchall()

    conn.close()

    return render_template('doar.html', doacoes=doacoes)


# ❌ EXCLUIR
@main.route('/excluir/<int:id>')
def excluir(id):
    if 'usuario' not in session:
        return redirect('/login')

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM doacoes WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    flash('Doação excluída com sucesso!')

    return redirect('/doar')


# ✏ EDITAR
@main.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario' not in session:
        return redirect('/login')

    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        item = request.form.get('item')
        quantidade = request.form.get('quantidade')

        if item and quantidade:
            cursor.execute(
                "UPDATE doacoes SET item = ?, quantidade = ? WHERE id = ?",
                (item, quantidade, id)
            )

            conn.commit()
            conn.close()

            flash('Doação atualizada com sucesso!')

            return redirect('/doar')

    cursor.execute("SELECT item, quantidade FROM doacoes WHERE id = ?", (id,))
    doacao = cursor.fetchone()

    conn.close()

    return render_template('editar.html', doacao=doacao, id=id)