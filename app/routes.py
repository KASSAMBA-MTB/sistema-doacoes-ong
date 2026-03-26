from flask import Blueprint, render_template, request, redirect

main = Blueprint('main', __name__)

doacoes = []

@main.route('/')
def home():
    return render_template('home.html')


@main.route('/doar', methods=['GET', 'POST'])
def doar():
    if request.method == 'POST':
        item = request.form.get('item')
        quantidade = request.form.get('quantidade')

        doacoes.append({
            'item': item,
            'quantidade': quantidade
        })

        return redirect('/doar')

    return render_template('doar.html', doacoes=doacoes)