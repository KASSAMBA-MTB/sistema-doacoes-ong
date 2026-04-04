# 🏢 Sistema de Gestão de Doações para ONGs

Este projeto é uma aplicação web desenvolvida com **Django + SQLite**, com o objetivo de gerenciar doações, permitindo cadastro, edição, exclusão e controle de acesso por login.

---

## 🚀 Funcionalidades

### 📦 Gestão de Doações (CRUD)
- ✅ Cadastrar doações
- ✅ Listar doações
- ✅ Editar doações
- ✅ Excluir doações com confirmação

### 🔐 Autenticação
- ✅ Login com usuário e senha
- ✅ Sessão de usuário
- ✅ Proteção de rotas
- ✅ Logout

### 💬 Experiência do Usuário
- ✅ Mensagens de feedback (flash messages)
- ✅ Confirmação antes de excluir
- ✅ Interface responsiva com Bootstrap

---

## 🧰 Tecnologias Utilizadas

- Python 3
- Django
- PostgreSQL
- HTML5
- Bootstrap 5
- Jinja2

---

## 📂 Estrutura do Projeto

Projeto criado e organizado da seguinte maneira:

```text
sistema_doacoes_ong/
├── .env
├── .env.example
├── .gitignore
├── manage.py
├── README.md
├── requirements.txt
├── apps/
│   ├── core/ < -- Toda a regra de negócio do sistema
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── core/
│   │   │       ├── base.html
│   │   │       └── home.html
│   │   ├── apps.py
│   │   ├── context_processors.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── dashboards/
│   │   ├── templates/
│   │   │   └── dashboards/
│   │   │       └── dashboard.html
│   │   ├── apps.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── doacoes/
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── doacoes/
│   │   │       ├── doar.html
│   │   │       ├── doar_cadastro.html
│   │   │       ├── doar_lista.html
│   │   │       └── editar.html
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   └── usuarios/
│       ├── migrations/
│       ├── templates/
│       │   └── usuarios/
│       │       ├── login.html
│       │       └── registro.html
│       ├── apps.py
│       ├── decorators.py
│       ├── models.py
│       ├── services.py
│       ├── urls.py
│       └── views.py
└── config/
	├── asgi.py
	├── settings.py
	├── settings_test.py
	├── urls.py
	└── wsgi.py
```
