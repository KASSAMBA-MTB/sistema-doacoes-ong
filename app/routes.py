from database import conectar
from flask import Blueprint, render_template, request, redirect

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')


@main.route('/doar', methods=['GET', 'POST'])
def doar():
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

        return redirect('/doar')

    # 🔥 BUSCA DO BANCO (COM ID)
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, item, quantidade FROM doacoes")
    doacoes = cursor.fetchall()

    conn.close()

    return render_template('doar.html', doacoes=doacoes)


# 🔥 ROTA DE EXCLUSÃO (FORA DA FUNÇÃO)
@main.route('/excluir/<int:id>')
def excluir(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM doacoes WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect('/doar')
@main.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        item = request.form.get('item')
        quantidade = request.form.get('quantidade')

        cursor.execute(
            "UPDATE doacoes SET item = ?, quantidade = ? WHERE id = ?",
            (item, quantidade, id)
        )

        conn.commit()
        conn.close()

        return redirect('/doar')

    # GET → buscar dados atuais
    cursor.execute("SELECT item, quantidade FROM doacoes WHERE id = ?", (id,))
    doacao = cursor.fetchone()

    conn.close()

    return render_template('editar.html', doacao=doacao, id=id)