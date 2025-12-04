# 6. Definições do Sistema

## 6.1 Tecnologias Utilizadas

### Frontend (UI)

**HTML, CSS, JavaScript**
- **HTML5**: Estruturação das páginas web
- **CSS3**: Estilização e design responsivo
- **JavaScript (ES6+)**: Interatividade, manipulação do DOM e comunicação com APIs

**Gráficos: Plotly.js**
- **Plotly.js**: Biblioteca JavaScript para visualização de gráficos interativos
  - Gráficos de barras
  - Gráficos de pizza
  - Gráficos de linha
  - Histogramas
  - Gráficos interativos com zoom, hover e download

**Frameworks e Bibliotecas Frontend:**
- **Bootstrap 5.3.2**: Framework CSS para layout responsivo e componentes UI
- **Shepherd.js**: Biblioteca para tutoriais interativos e suporte ao usuário
- **Google Fonts (Inter)**: Tipografia do sistema

---

### Backend (Lógica de Negócio)

**Flask**
- **Flask 3.0.0**: Framework web Python para desenvolvimento do backend
- **Flask-Login 0.6.3**: Gerenciamento de sessões e autenticação de usuários
- **Flask-Mail 0.9.1**: Envio de emails (boas-vindas, recuperação de senha)
- **Flask-SQLAlchemy 3.1.1**: ORM (Object-Relational Mapping) para interação com banco de dados
- **Flask-Bcrypt 1.0.1**: Hash seguro de senhas

**Processamento de Dados:**
- **Pandas 2.1.4**: Biblioteca Python para análise e manipulação de dados
  - Leitura e processamento de arquivos CSV
  - Filtragem e agrupamento de dados
  - Análise estatística básica
- **NumPy 1.26.2**: Operações matemáticas e numéricas
- **Plotly 5.18.0**: Geração de gráficos no backend (Plotly Express)
  - Criação de gráficos programaticamente
  - Conversão para formato JSON para transmissão ao frontend

**Segurança:**
- **itsdangerous 2.1.2**: Geração de tokens seguros para recuperação de senha
- **python-dotenv 1.0.0**: Gerenciamento de variáveis de ambiente

**Banco de Dados:**
- **PyMySQL 1.1.0**: Driver Python para conexão com MySQL

---

### Banco de Dados

**MySQL**
- Sistema de gerenciamento de banco de dados relacional
- Armazenamento de dados de usuários, logs e tokens de recuperação

**SQLAlchemy ORM (via Flask-SQLAlchemy)**
- Mapeamento objeto-relacional para Python
- Abstração de consultas SQL
- Gerenciamento de relacionamentos entre tabelas
- Migrações e versionamento de esquema

**Estrutura de Tabelas:**
- `usuario`: Dados dos usuários do sistema
- `log`: Logs de atividades para auditoria
- `recuperacao_senha`: Tokens temporários para recuperação de senha

---

### Comunicação

**API REST (Flask)**
- Endpoints RESTful para comunicação entre frontend e backend
- Formato de dados: **JSON**
- Métodos HTTP utilizados:
  - **GET**: Para renderização de páginas e obtenção de dados
  - **POST**: Para envio de formulários, uploads e chamadas de API

**Endpoints Principais:**
- `/api/columns`: Obtém informações sobre colunas de arquivos CSV
- `/api/grafico`: Gera gráficos baseados em parâmetros fornecidos
- `/api/save_chart`: Salva gráficos gerados como imagens PNG
- `/upload`: Endpoint para upload de arquivos CSV

**Protocolo:**
- HTTP/HTTPS
- Headers: `Content-Type: application/json` para requisições JSON
- Cookies de sessão gerenciados automaticamente pelo Flask-Login

---

### Outras Ferramentas

**Desenvolvimento:**
- **VSCode**: Editor de código utilizado no desenvolvimento
- **Git**: Controle de versão do código-fonte
- **GitHub**: Repositório remoto e hospedagem do código
  - GitHub Pages: Hospedagem do protótipo de alta fidelidade

**Design e Prototipagem:**
- **Figma**: Ferramenta para criação do protótipo de alta fidelidade
- **Canva**: Criação de elementos visuais e materiais de design

**Armazenamento e Colaboração:**
- **Google Drive**: Armazenamento de arquivos e documentos do projeto
- **GitHub**: Versionamento e colaboração no código

**Ambiente de Desenvolvimento:**
- **Python 3.x**: Linguagem de programação do backend
- **pip**: Gerenciador de pacotes Python
- **venv**: Ambiente virtual Python para isolamento de dependências

---

## 6.2 Versões Específicas das Tecnologias

### Backend (Python)
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

### Frontend (CDN)
```
Bootstrap: 5.3.2
Plotly.js: 2.32.0
Shepherd.js: (versão mais recente via CDN)
```

---

## 6.3 Arquitetura de Tecnologias

```
┌─────────────────────────────────────┐
│         FRONTEND (Cliente)          │
├─────────────────────────────────────┤
│ HTML5 + CSS3 + JavaScript           │
│ Bootstrap 5.3.2                    │
│ Plotly.js 2.32.0                   │
│ Shepherd.js                         │
└──────────────┬──────────────────────┘
               │ HTTP/HTTPS + JSON
               │
┌──────────────▼──────────────────────┐
│      BACKEND (Servidor Flask)        │
├─────────────────────────────────────┤
│ Flask 3.0.0                         │
│ Flask-Login, Flask-Mail, etc.       │
│ Pandas 2.1.4                        │
│ Plotly 5.18.0                       │
│ NumPy 1.26.2                        │
└──────────────┬──────────────────────┘
               │ SQLAlchemy ORM
               │
┌──────────────▼──────────────────────┐
│      BANCO DE DADOS (MySQL)          │
├─────────────────────────────────────┤
│ MySQL                                │
│ SQLAlchemy ORM                      │
└─────────────────────────────────────┘
```

---

## 6.4 Notas Importantes

1. **Flask vs Django**: O sistema utiliza **Flask**, não Django. Embora ambos sejam frameworks Python para web, Flask é mais leve e flexível, enquanto Django é mais completo e opinativo.

2. **MySQL vs PostgreSQL**: O sistema utiliza **MySQL** como banco de dados, não PostgreSQL. Ambos são bancos relacionais robustos, mas MySQL foi escolhido para este projeto.

3. **Plotly vs Seaborn/Matplotlib**: O sistema utiliza **Plotly** (tanto no backend quanto no frontend) para geração de gráficos, oferecendo gráficos interativos nativamente, diferentemente de Seaborn/Matplotlib que geram gráficos estáticos.

4. **API REST**: A API REST é implementada nativamente com Flask, sem necessidade de frameworks adicionais como Django REST Framework, pois Flask já oferece suporte completo para criação de APIs RESTful.

5. **ORM**: O sistema utiliza **SQLAlchemy** via Flask-SQLAlchemy, não Django ORM. SQLAlchemy é um ORM independente e mais flexível que o Django ORM.

---

## 6.5 Requisitos do Sistema

**Servidor:**
- Python 3.8 ou superior
- MySQL 5.7 ou superior
- Servidor web (ex: Gunicorn, uWSGI) para produção

**Cliente:**
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- JavaScript habilitado
- Conexão com internet (para CDNs)

**Desenvolvimento:**
- Python 3.x
- pip (gerenciador de pacotes)
- Git
- Editor de código (VSCode recomendado)

