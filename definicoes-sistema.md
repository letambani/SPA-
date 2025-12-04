# 6. Definições do Sistema

## 6.1 Tecnologias Utilizadas

### Frontend (UI)

**Linguagens e Frameworks:**
- **HTML5**: Estruturação das páginas web
- **CSS3**: Estilização e design responsivo
- **JavaScript (ES6+)**: Interatividade e manipulação do DOM

**Bibliotecas e Frameworks Frontend:**
- **Bootstrap 5.3.2**: Framework CSS para layout responsivo e componentes UI
- **Plotly.js 2.32.0**: Biblioteca JavaScript para visualização de gráficos interativos (barras, pizza, linha, histograma)
- **Shepherd.js**: Biblioteca para criação de tutoriais interativos e suporte ao usuário

**Gráficos:**
- **Plotly.js**: Renderização de gráficos interativos no frontend
- **Plotly Express (Python)**: Geração de gráficos no backend que são convertidos para JSON e renderizados no frontend

**Sistema de Templates:**
- **Jinja2**: Motor de templates do Flask para renderização dinâmica de HTML

---

### Backend (Lógica de Negócio)

**Framework Web:**
- **Flask 3.0.0**: Framework web Python para desenvolvimento do backend

**Extensões Flask:**
- **Flask-Login 0.6.3**: Gerenciamento de sessões e autenticação de usuários
- **Flask-SQLAlchemy 3.1.1**: ORM (Object-Relational Mapping) para interação com banco de dados
- **Flask-Bcrypt 1.0.1**: Hash seguro de senhas usando algoritmo Bcrypt
- **Flask-Mail 0.9.1**: Envio de emails (boas-vindas, recuperação de senha)

**Processamento de Dados:**
- **Pandas 2.1.4**: Manipulação e análise de dados CSV
- **NumPy 1.26.2**: Operações matemáticas e numéricas
- **Plotly 5.18.0**: Geração de gráficos no backend (Plotly Express)

**Segurança:**
- **itsdangerous 2.1.2**: Geração de tokens seguros para recuperação de senha

**Banco de Dados:**
- **PyMySQL 1.1.0**: Driver Python para conexão com MySQL

**Utilitários:**
- **python-dotenv 1.0.0**: Gerenciamento de variáveis de ambiente

---

### Banco de Dados

**Sistema de Gerenciamento:**
- **MySQL**: Sistema de gerenciamento de banco de dados relacional

**ORM:**
- **SQLAlchemy**: ORM utilizado via Flask-SQLAlchemy para abstração do banco de dados
- **Django ORM**: Não utilizado (o sistema usa Flask, não Django)

**Estrutura:**
- Tabelas principais: `usuario`, `log`, `recuperacao_senha`
- Relacionamentos configurados via SQLAlchemy

---

### Comunicação

**API:**
- **API REST**: Endpoints RESTful implementados com Flask
- **Django REST Framework**: Não utilizado (o sistema usa Flask nativo)

**Formato de Dados:**
- **JSON**: Formato principal de troca de dados entre frontend e backend
- **HTTP/HTTPS**: Protocolo de comunicação
- **FormData**: Para upload de arquivos CSV

**Endpoints Principais:**
- `/api/columns` - Obter colunas de arquivo CSV
- `/api/grafico` - Gerar gráficos baseados em parâmetros
- `/api/save_chart` - Salvar gráficos como PNG
- `/upload` - Upload de arquivos CSV

---

### Outras Ferramentas

**Desenvolvimento:**
- **VSCode**: Editor de código utilizado no desenvolvimento
- **Cursor**: Editor de código com IA integrada
- **Git**: Controle de versão
- **GitHub**: Repositório remoto e hospedagem do código

**Design e Prototipagem:**
- **Figma**: Ferramenta de design para criação de protótipos de alta fidelidade
- **Canva**: Ferramenta auxiliar para criação de elementos visuais

**Armazenamento e Colaboração:**
- **Google Drive**: Armazenamento de arquivos e documentos do projeto

**IA e Assistência:**
- **ChatGPT**: Assistência em desenvolvimento e resolução de problemas
- **Devin**: Ferramenta de IA para desenvolvimento

---

## 6.2 Versões Específicas

### Python
- **Python 3.x**: Linguagem de programação do backend

### Dependências Principais (requirements.txt)
```
Flask==3.0.0
Flask-Login==0.6.3
Flask-Mail==0.9.1
Flask-SQLAlchemy==3.1.1
Flask-Bcrypt==1.0.1
itsdangerous==2.1.2
pandas==2.1.4
numpy==1.26.2
plotly==5.18.0
PyMySQL==1.1.0
python-dotenv==1.0.0
```

### Bibliotecas Frontend (via CDN)
- Bootstrap 5.3.2
- Plotly.js 2.32.0
- Shepherd.js (versão mais recente)

---

## 6.3 Arquitetura de Tecnologias

**Stack Tecnológico:**
- **Frontend**: HTML5 + CSS3 + JavaScript + Bootstrap + Plotly.js
- **Backend**: Python + Flask + Pandas + Plotly
- **Banco de Dados**: MySQL + SQLAlchemy ORM
- **Comunicação**: REST API (JSON)
- **Templates**: Jinja2 (Flask)

**Padrão Arquitetural:**
- Arquitetura em camadas (Layered Architecture)
- Separação de responsabilidades (Frontend, Backend, Banco de Dados)
- API RESTful para comunicação cliente-servidor

---

## 6.4 Notas Importantes

1. **Flask vs Django**: O sistema utiliza **Flask**, não Django. Embora ambos sejam frameworks Python para web, Flask é mais leve e flexível, enquanto Django é mais completo e opinativo.

2. **MySQL vs PostgreSQL**: O sistema utiliza **MySQL**, não PostgreSQL. Ambos são bancos relacionais, mas têm diferenças em sintaxe e recursos.

3. **Plotly**: Utilizado tanto no backend (Python) quanto no frontend (JavaScript) para geração e renderização de gráficos interativos.

4. **Templates Jinja2**: O Flask utiliza Jinja2 como motor de templates, que tem sintaxe similar ao Django, mas são sistemas diferentes.

5. **ORM SQLAlchemy**: Utilizado via Flask-SQLAlchemy, não Django ORM. SQLAlchemy é mais flexível e pode ser usado independentemente do framework.

