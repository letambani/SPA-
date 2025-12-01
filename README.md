# SPA - Sistema de Perfil Discente FMPSC

Sistema web desenvolvido em Flask para análise de dados e perfil discente da Faculdade Municipal de Palhoça (FMPSC).

## 📋 Descrição

O SPA (Sistema de Perfil Discente) é uma plataforma web que permite:
- Cadastro e autenticação de usuários
- Upload e análise de arquivos CSV
- Geração de gráficos interativos (barras, pizza, linha, histograma)
- Comparação entre diferentes conjuntos de dados
- Recuperação de senha via e-mail
- Sistema de logs de atividades

## 🚀 Tecnologias

- **Backend**: Flask (Python)
- **Banco de Dados**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Visualização**: Plotly.js
- **Autenticação**: Flask-Login
- **E-mail**: Flask-Mail

## 📦 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd projeto_fmpscGit
```

2. Crie um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o arquivo `config.py` com suas credenciais:
   - SECRET_KEY
   - SQLALCHEMY_DATABASE_URI (MySQL)
   - Configurações de e-mail (MAIL_USERNAME, MAIL_PASSWORD)

5. Crie o banco de dados:
```bash
python app.py
```
(O banco será criado automaticamente na primeira execução)

## 🏃 Executando

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## 📁 Estrutura do Projeto

```
projeto_fmpscGit/
├── app.py                 # Aplicação principal Flask
├── config.py              # Configurações
├── requirements.txt       # Dependências Python
├── models/                # Modelos de dados
│   ├── user.py
│   ├── log.py
│   └── recuperacao_senha.py
├── templates/             # Templates HTML
│   ├── index.html
│   ├── login.html
│   ├── cadastro.html
│   └── ...
├── static/                # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── logo.png
├── uploads/               # Arquivos CSV enviados
└── saved_charts/          # Gráficos salvos
```

## 🔐 Funcionalidades

### Autenticação
- Login com e-mail institucional (@fmpsc.edu.br)
- Cadastro com validação de CPF
- Recuperação de senha via e-mail
- Sistema de sessão com Flask-Login

### Análise de Dados
- Upload de arquivos CSV
- Seleção de colunas para análise
- Geração de gráficos interativos
- Comparação entre arquivos
- Filtros dinâmicos
- Agrupamento de dados
- Exportação de gráficos

### Segurança
- Hash de senhas com Bcrypt
- Tokens seguros para recuperação de senha
- Validação server-side de dados
- Sistema de logs de atividades

## 👥 Desenvolvido por

iLab - Ambiente de Inovação e Desenvolvimento

## 📄 Licença

Este projeto é de uso interno da FMPSC.

