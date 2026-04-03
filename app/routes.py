from flask import Blueprint, render_template, request, redirect, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from database import conectar

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

main = Blueprint('main', __name__)

@main.route('/')
def teste():
    return "OK FUNCIONANDO"


# 🔐 PROTEÇÃO
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            flash('Faça login para acessar o sistema')
            return redirect('/login?next=' + request.path)
        return func(*args, **kwargs)
    return wrapper


# 🏠 HOME
@main.route('/')
def home():
    return redirect('/login')


# 🔐 LOGIN
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        senha = request.form.get('senha', '').strip()

        if not usuario or not senha:
            flash('Preencha todos os campos')
            return redirect('/login')

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

            next_page = request.form.get('next') or request.args.get('next')

            # 🔥 CORREÇÃO FINAL (evita /None e garante rota válida)
            if not next_page or not next_page.startswith('/'):
                next_page = '/dashboard'

            return redirect(next_page)

        else:
            flash('Usuário ou senha inválidos')
            return redirect('/login')

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


# 📦 DOAÇÕES
@main.route('/doar', methods=['GET', 'POST'])
@login_required
def doar():
    conn = conectar()
    cursor = conn.cursor()

    busca = request.args.get('busca')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

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

    query = "SELECT id, item, quantidade, data FROM doacoes WHERE 1=1"
    query += " ORDER BY data DESC"
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
    dados = cursor.fetchall()

    from datetime import datetime

    doacoes = [
        {
            "id": d[0],
            "item": d[1],
            "quantidade": d[2],
            "data": datetime.strptime(d[3], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M") if d[3] else None
        }
        for d in dados
    ] 
    conn.close()

    return render_template(
        'doar.html',
        doacoes=doacoes,
        busca=busca,
        data_inicio=data_inicio,
        data_fim=data_fim
    )


# ❌ EXCLUIR
@main.route('/excluir/<int:id>', methods=['POST'])
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


@main.route('/dashboard')
@login_required
def dashboard():
    conn = conectar()
    cursor = conn.cursor()

    # KPIs
    cursor.execute("SELECT COUNT(*) FROM doacoes")
    total_doacoes = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(quantidade) FROM doacoes")
    total_itens = cursor.fetchone()[0] or 0

    # AGRUPAMENTO + ORDENAÇÃO
    cursor.execute("""
        SELECT item, SUM(quantidade) as total
        FROM doacoes
        GROUP BY item
        ORDER BY total DESC
    """)

    dados = cursor.fetchall()

    # TOP 3 ITENS
    top_itens = []
    if dados:
        top_itens = dados[:3]

    # LISTAS PARA GRÁFICO
    labels = []
    valores = []

    if dados:
        for item, quantidade in dados:
            labels.append(item)
            valores.append(quantidade)

    conn.close()

    return render_template(
        'dashboard.html',
        total_doacoes=total_doacoes,
        total_itens=total_itens,
        labels=labels,
        valores=valores,
        top_itens=top_itens
    )