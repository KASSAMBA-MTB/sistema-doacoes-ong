from flask import Blueprint, render_template, request, redirect, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from database import conectar

main = Blueprint('main', __name__)


# 🔐 PROTEÇÃO
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            flash('Faça login para acessar o sistema')
            return redirect('/login')
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# 🔐 LOGIN
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT usuario, senha FROM usuarios WHERE usuario = ?",
            (usuario,)
        )

        resultado = cursor.fetchone()
        conn.close()

        if resultado and check_password_hash(resultado[1], senha):
            session['usuario'] = resultado[0]
            flash('Login realizado com sucesso!')
            return redirect('/dashboard')
        else:
            flash('Usuário ou senha inválidos')

    return render_template('login.html')


# 📝 REGISTRO
@main.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if not usuario or not senha:
            flash('Preencha todos os campos')
            return redirect('/registro')

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = ?",
            (usuario,)
        )
        existente = cursor.fetchone()

        if existente:
            conn.close()
            flash('Usuário já existe')
            return redirect('/registro')

        senha_hash = generate_password_hash(senha)

        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            (usuario, senha_hash)
        )

        conn.commit()
        conn.close()

        flash('Usuário cadastrado com sucesso!')
        return redirect('/login')

    return render_template('registro.html')


# 🔓 LOGOUT
@main.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!')
    return redirect('/login')


# 🏠 HOME
@main.route('/')
def home():
    return redirect('/login')


# 📦 DOAÇÕES
@main.route('/doar', methods=['GET', 'POST'])
@login_required
def doar():
    conn = conectar()
    cursor = conn.cursor()

    # 🔎 Captura filtros
    busca = request.args.get('busca')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    # 📦 CADASTRO
    if request.method == 'POST':
        item = request.form.get('item')
        quantidade = request.form.get('quantidade')

        if item and quantidade:
            cursor.execute(
                "INSERT INTO doacoes (item, quantidade, data) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (item, quantidade)
            )
            conn.commit()
            flash('Doação cadastrada com sucesso!')
            return redirect('/doar')

    # 🔥 CONSULTA COM FILTRO COMPLETO
    query = "SELECT id, item, quantidade, data FROM doacoes WHERE 1=1"
    params = []

    if busca:
        query += " AND item LIKE ?"
        params.append(f"%{busca}%")

    if data_inicio:
        query += " AND date(data) >= date(?)"
        params.append(data_inicio)

    if data_fim:
        query += " AND date(data) <= date(?)"
        params.append(data_fim)

    cursor.execute(query, params)
    doacoes = cursor.fetchall()

    conn.close()

    return render_template(
        'doar.html',
        doacoes=doacoes,
        busca=busca,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

# ❌ EXCLUIR
@main.route('/excluir/<int:id>')
@login_required
def excluir(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM doacoes WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    flash('Doação excluída com sucesso!')
    return redirect('/doar')


# ✏ EDITAR
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

            flash('Doação atualizada com sucesso!')
            return redirect('/doar')

    cursor.execute(
        "SELECT item, quantidade FROM doacoes WHERE id = ?",
        (id,)
    )
    doacao = cursor.fetchone()

    conn.close()

    return render_template('editar.html', doacao=doacao, id=id)


# 📊 DASHBOARD (VERSÃO BLINDADA)
@main.route('/dashboard')
@login_required
def dashboard():
    conn = conectar()
    cursor = conn.cursor()

    # Totais
    cursor.execute("SELECT COUNT(*) FROM doacoes")
    total_doacoes = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(quantidade) FROM doacoes")
    total_itens = cursor.fetchone()[0] or 0

    # 📊 Dados do gráfico
    cursor.execute("""
        SELECT item, SUM(quantidade)
        FROM doacoes
        GROUP BY item
    """)

    dados = cursor.fetchall()

    labels = []
    valores = []

    if dados:
        for item, quantidade in dados:
            labels.append(item)
            valores.append(quantidade)

    conn.close()

    return render_template(
        "dashboard.html",
        total_doacoes=total_doacoes,
        total_itens=total_itens,
        labels=labels,
        valores=valores
    )