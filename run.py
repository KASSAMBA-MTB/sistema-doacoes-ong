from app import create_app

app = create_app()


if __name__ == '__main__':
    from database import (
        criar_tabela_doacoes,
        criar_tabela_usuarios,
        criar_usuario_padrao
    )

    # 🔧 Inicialização do banco (executa só localmente)
    criar_tabela_doacoes()
    criar_tabela_usuarios()
    criar_usuario_padrao()

    app.run(host='0.0.0.0', port=5001, debug=True)