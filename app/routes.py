from flask import Blueprint, render_template, request, redirect, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import datetime
from database import conectar

main = Blueprint('main', __name__)

# 🔐 LOGIN REQUIRED DECORATOR
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            flash('Faça login para acessar o sistema', 'warning')
            return redirect('/login?next=' + request.path)
        return func(*args, **kwargs)
    return wrapper

# 🏠 HOME
@main.route('/')
def home():
    return redirect('/dashboard')

# 🔐 LOGIN
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        senha = request.form.get('senha', '').strip()

        if not usuario or not senha:
            flash('Preencha todos os campos', 'warning')
            return redirect('/login')

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, senha FROM usuarios WHERE usuario = ?", (usuario,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado and check_password_hash(resultado[1], senha):
            session['usuario'] = resultado[0]
            flash('Login realizado com sucesso!', 'success')

            next_page = request.form.get('next') or request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = '/dashboard'
            return redirect(next_page)
        else:
            flash('Usuário ou senha inválidos', 'danger')
            return redirect('/login')

    return render_template('login.html')

# 📝 REGISTRO
@main.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if not usuario or not senha:
            flash('Preencha todos os campos', 'warning')
            return redirect('/registro')

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        existente = cursor.fetchone()

        if existente:
            conn.close()
            flash('Usuário já existe', 'danger')
            return redirect('/registro')

        senha_hash = generate_password_hash(senha)
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha_hash))
        conn.commit()
        conn.close()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect('/login')

    return render_template('registro.html')

# 🔓 LOGOUT
@main.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect('/login')

# 📦 LISTA DE DOAÇÕES
@main.route('/doar')
@login_required
def listar_doacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, item, quantidade, data FROM doacoes ORDER BY data DESC")
    dados = cursor.fetchall()

    doacoes = [
        {
            "id": d[0],
            "item": d[1],
            "quantidade": d[2],
            "data": datetime.strptime(d[3], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M") if d[3] else "-"
        }
        for d in dados
    ]
    conn.close()

    return render_template('doar_lista.html', doacoes=doacoes, active='lista')

# 📄 FORMULÁRIO DE CADASTRO
@main.route('/doar/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_doacao():
    if request.method == 'POST':
        item = request.form.get('item')
        quantidade = request.form.get('quantidade')

        if item and quantidade:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO doacoes (item, quantidade, data) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (item, quantidade)
            )
            conn.commit()
            conn.close()
            flash('Doação cadastrada com sucesso!', 'success')
            return redirect('/doar')

    return render_template('doar_cadastro.html', active='cadastro')

# ❌ EXCLUIR DOAÇÃO
@main.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doacoes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Doação excluída com sucesso!', 'success')
    return redirect('/doar')

# ✏ EDITAR DOAÇÃO
@main.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
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
            flash('Doação atualizada com sucesso!', 'success')
            return redirect('/doar')

    cursor.execute("SELECT item, quantidade FROM doacoes WHERE id = ?", (id,))
    doacao = cursor.fetchone()
    conn.close()
    return render_template('editar.html', doacao=doacao, id=id)

# 📊 DASHBOARD
@main.route('/dashboard')
@login_required
def dashboard():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM doacoes")
    total_doacoes = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(quantidade) FROM doacoes")
    total_itens = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT item, SUM(quantidade) as total
        FROM doacoes
        GROUP BY item
        ORDER BY total DESC
    """)
    dados = cursor.fetchall()
    conn.close()

    top_itens = dados[:3] if dados else []

    labels = [d[0] for d in dados] if dados else []
    valores = [d[1] for d in dados] if dados else []

    return render_template(
        'dashboard.html',
        total_doacoes=total_doacoes,
        total_itens=total_itens,
        labels=labels,
        valores=valores,
        top_itens=top_itens
    )
