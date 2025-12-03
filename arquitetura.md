# 5. Arquitetura

## 5.1 Camada de Apresentação (Frontend)

**Responsabilidade:** Interface com o usuário, visualização de gráficos, formulários de login/cadastro, navegação e filtros.

**Tecnologias Utilizadas:**
- **HTML5/CSS3**: Estrutura e estilização das páginas
- **JavaScript (ES6+)**: Interatividade, manipulação do DOM e comunicação com APIs
- **Bootstrap 5**: Framework CSS para layout responsivo e componentes UI
- **Plotly.js**: Biblioteca JavaScript para visualização de gráficos interativos (barras, pizza, linha, histograma)
- **Shepherd.js**: Biblioteca para tutoriais interativos e suporte ao usuário

**Componentes Principais:**
- **Páginas de Autenticação**: Login, Cadastro, Recuperação de Senha, Reset de Senha
- **Dashboard de Análises**: Interface principal com painel lateral de configurações e área de visualização de gráficos
- **Sistema de Filtros**: Filtros dinâmicos baseados nas colunas dos arquivos CSV carregados
- **Upload de Arquivos**: Interface para envio de arquivos CSV via modal
- **Navegação**: Menu fixo no topo para acesso rápido a todas as páginas do sistema

**Funcionalidades Frontend:**
- Validação client-side de formulários (CPF, email institucional, senha)
- Máscaras de entrada (formatação automática de CPF)
- Toggle de visibilidade de senha
- Atualização dinâmica de seletores baseada em escolhas do usuário
- Geração e renderização de gráficos interativos via Plotly.js
- Feedback visual (mensagens de sucesso/erro, estados de loading)
- Responsividade para dispositivos móveis e desktop

---

## 5.2 Camada de Lógica de Negócio (Backend)

**Responsabilidade:** Processamento dos dados, lógica de filtros, geração de gráficos e autenticação de usuários.

**Tecnologias Utilizadas:**
- **Flask**: Framework web Python para desenvolvimento do backend
- **Flask-Login**: Gerenciamento de sessões e autenticação de usuários
- **Flask-Bcrypt**: Hash seguro de senhas
- **Flask-Mail**: Envio de emails (boas-vindas, recuperação de senha)
- **Pandas**: Processamento e análise de dados CSV
- **Plotly Express**: Geração de gráficos no backend
- **NumPy**: Operações matemáticas e numéricas
- **itsdangerous**: Geração de tokens seguros para recuperação de senha

**Autenticação:**
Flask-Login fornece ferramentas para criação de login/cadastro e proteção das páginas. O sistema implementa:
- Validação de credenciais (email e senha)
- Hash de senhas com Bcrypt (nunca armazenadas em texto plano)
- Sessões de usuário gerenciadas automaticamente
- Proteção de rotas com decorator `@login_required`
- Validação de email institucional (@fmpsc.edu.br ou @aluno.fmpsc.edu.br)
- Validação matemática de CPF (algoritmo de dígitos verificadores)
- Sistema de tokens temporários para recuperação de senha (expiração em 60 minutos)

**Processamento de Dados:**
- **Upload de CSV**: Validação e armazenamento de arquivos CSV na pasta `uploads/`
- **Análise de Dados**: Leitura e processamento de arquivos CSV com Pandas
- **Geração de Gráficos**: Criação de gráficos (barras, pizza, linha, histograma) baseados nas colunas selecionadas
- **Comparação de Dados**: Lógica para comparar dois arquivos CSV e gerar gráficos de variação percentual
- **Agrupamento**: Suporte a agrupamento de dados por colunas específicas
- **Filtros**: Aplicação de filtros dinâmicos nos dados antes da geração de gráficos

**Filtros e Interatividade:**
A lógica de filtragem permite que os usuários:
- Selecionem arquivos CSV para análise
- Escolham colunas específicas para visualização
- Apliquem filtros por valores específicos de colunas
- Agrupem dados por categorias
- Comparem diferentes arquivos CSV
- Visualizem gráficos detalhados e interativos (RF-03)

**Rotas Principais:**
- `/login` - Autenticação de usuários
- `/cadastro` - Registro de novos usuários
- `/recuperar_senha` - Solicitação de recuperação de senha
- `/reset_senha/<token>` - Redefinição de senha via token
- `/analises` - Dashboard principal de análises
- `/upload` - Endpoint para upload de arquivos CSV
- `/api/columns` - API para obter colunas de um arquivo CSV
- `/api/grafico` - API para gerar gráficos baseados em parâmetros
- `/api/save_chart` - API para salvar gráficos gerados
- `/download_chart/<filename>` - Download de gráficos salvos

---

## 5.3 Camada de Persistência de Dados (Banco de Dados)

**Responsabilidade:** Armazenamento e recuperação dos dados dos usuários, logs de atividades e tokens de recuperação.

**Tecnologias Utilizadas:**
- **MySQL**: Sistema de gerenciamento de banco de dados relacional
- **SQLAlchemy**: ORM (Object-Relational Mapping) para Python
- **Flask-SQLAlchemy**: Extensão Flask para integração com SQLAlchemy

**Estrutura de Dados:**

### Tabela: `usuario`
Armazena informações dos usuários do sistema:
- **id** (Integer, Primary Key): Identificador único do usuário
- **nome** (String 100): Nome completo do usuário
- **email** (String 120, Unique): E-mail institucional do usuário
- **cargo** (String 50): Cargo/função do usuário no sistema
- **senha_hash** (String 128): Hash da senha (gerado com Bcrypt)
- **cpf** (String 14, Unique, Nullable): CPF do usuário no formato 000.000.000-00
- **data_cadastro** (DateTime): Data e hora do cadastro (padrão: UTC)
- **status** (Enum): Status do usuário (ATIVO, INATIVO, BLOQUEADO)

### Tabela: `log`
Armazena logs de atividades dos usuários para auditoria:
- **id** (Integer, Primary Key): Identificador único do log
- **id_usuario** (Integer, Foreign Key): Referência ao usuário
- **acao** (String): Tipo de ação realizada (ex: "Login", "Cadastro", "Recuperação de Senha")
- **descricao** (String): Descrição detalhada da ação
- **ip** (String): Endereço IP de origem da requisição
- **data_hora** (DateTime): Data e hora da ação (padrão: UTC)

### Tabela: `recuperacao_senha`
Armazena tokens temporários para recuperação de senha:
- **id** (Integer, Primary Key): Identificador único
- **id_usuario** (Integer, Foreign Key): Referência ao usuário
- **token** (String, Unique): Token único para recuperação
- **data_criacao** (DateTime): Data de criação do token
- **data_expiracao** (DateTime): Data de expiração do token (60 minutos após criação)

**Relacionamentos:**
- Um usuário pode ter múltiplos logs (relação 1:N)
- Um usuário pode ter múltiplos tokens de recuperação (relação 1:N)
- Relacionamentos configurados via SQLAlchemy com `backref` e `lazy=True`

**Segurança:**
- Senhas nunca são armazenadas em texto plano, apenas hashes gerados com Bcrypt
- Tokens de recuperação têm expiração automática
- Validação de unicidade para email e CPF
- Proteção contra SQL Injection via ORM SQLAlchemy

---

## 5.4 Camada de Comunicação (API/HTTP)

**Responsabilidade:** Facilitar a comunicação entre o backend e o frontend, bem como o processamento de requisições de dados.

**Protocolo:** HTTP/HTTPS

**Formato de Dados:**
**JSON**: O formato de troca de dados entre frontend e backend é JSON, especialmente para:
- Interatividade com os gráficos (dados enviados e recebidos via JSON)
- Filtros dinâmicos (parâmetros de filtro enviados como JSON)
- Respostas de APIs (estrutura padronizada em JSON)
- Upload de arquivos (respostas em JSON indicando sucesso/erro)

**Endpoints da API:**

### POST `/api/columns`
Recebe o nome do arquivo CSV e retorna informações sobre suas colunas:
```json
Request: {"filename": "arquivo.csv"}
Response: {
  "columns": [
    {
      "name": "Coluna1",
      "is_numeric": true,
      "unique_values_count": 10,
      "sample_values": ["valor1", "valor2", ...]
    }
  ]
}
```

### POST `/api/grafico`
Gera gráficos baseados em parâmetros fornecidos:
```json
Request: {
  "filename": "arquivo.csv",
  "coluna": "NomeColuna",
  "tipo": "bar",
  "filtros": {"ColunaFiltro": ["valor1", "valor2"]},
  "groupby": "ColunaAgrupamento",
  "compare_with": "arquivo2.csv" (opcional)
}
Response: {
  "graficos": [
    {
      "title": "Título do Gráfico",
      "fig": { /* Objeto Plotly JSON */ }
    }
  ]
}
```

### POST `/upload`
Endpoint para upload de arquivos CSV:
```json
Request: FormData com arquivo
Response: {"success": true} ou {"success": false, "error": "mensagem"}
```

### POST `/api/save_chart`
Salva um gráfico gerado como imagem PNG:
```json
Request: {"data_url": "data:image/png;base64,..."}
Response: {"saved": true, "file": "chart_abc123.png"}
```

**Métodos HTTP Utilizados:**
- **GET**: Para renderização de páginas HTML
- **POST**: Para envio de formulários, uploads e chamadas de API
- **GET com parâmetros**: Para download de arquivos e acesso a recursos

**Headers Importantes:**
- `Content-Type: application/json` para requisições JSON
- `Content-Type: multipart/form-data` para upload de arquivos
- Cookies de sessão gerenciados automaticamente pelo Flask-Login

---

## 5.5 Fluxo do Sistema

### 5.5.1 Login/Cadastro
O usuário (coordenador, diretor, etc.) se autentica no sistema:
1. Usuário acessa a página de login (`/login`)
2. Informa email institucional e senha
3. Sistema valida credenciais no banco de dados
4. Se válido, cria sessão de usuário e redireciona para dashboard
5. Se inválido, exibe mensagem de erro
6. Sistema registra ação de login na tabela `log`

**Fluxo de Cadastro:**
1. Usuário acessa página de cadastro (`/cadastro`)
2. Preenche formulário (nome, CPF, email, cargo, senha)
3. Sistema valida:
   - Formato de email institucional (@fmpsc.edu.br)
   - CPF (formato e dígitos verificadores)
   - Unicidade de email e CPF
   - Senha (mínimo 8 caracteres)
4. Se válido, cria usuário no banco, gera hash da senha e envia email de boas-vindas
5. Redireciona para página de login

### 5.5.2 Visualização de Dados
O usuário é direcionado para o painel onde visualiza gráficos interativos sobre o perfil discente:
1. Após login bem-sucedido, usuário é redirecionado para `/analises`
2. Sistema lista arquivos CSV disponíveis na pasta `uploads/`
3. Usuário seleciona um arquivo base para análise
4. Frontend faz requisição AJAX para `/api/columns` para obter colunas do arquivo
5. Sistema retorna informações sobre colunas (nome, tipo, valores únicos)
6. Frontend atualiza seletores dinamicamente

### 5.5.3 Interação com Gráficos
O usuário pode aplicar filtros (por curso, por desempenho, etc.) para ver gráficos específicos:
1. Usuário seleciona:
   - Arquivo CSV base
   - Coluna principal para análise
   - Tipo de gráfico (barras, pizza, linha, histograma)
   - Filtros opcionais (valores específicos de colunas)
   - Agrupamento opcional (por categoria)
   - Arquivo de comparação (opcional)
2. Frontend envia requisição POST para `/api/grafico` com parâmetros em JSON
3. Backend processa:
   - Carrega arquivo CSV com Pandas
   - Aplica filtros selecionados
   - Agrupa dados se especificado
   - Gera gráfico com Plotly Express
   - Se houver comparação, gera gráficos adicionais e cálculo de variação percentual
4. Backend retorna dados do gráfico em formato Plotly JSON
5. Frontend renderiza gráfico interativo usando Plotly.js
6. Usuário pode interagir com gráfico (zoom, hover, download)
7. Usuário pode salvar gráfico como PNG via `/api/save_chart`

**Fluxo de Comparação:**
1. Usuário seleciona dois arquivos CSV diferentes
2. Sistema valida que ambos têm a coluna selecionada
3. Gera três gráficos:
   - Gráfico do arquivo base
   - Gráfico do arquivo comparador
   - Gráfico de variação percentual entre os dois
4. Exibe todos os gráficos lado a lado para análise comparativa

### 5.5.4 Análise e Ação
O coordenador ou diretor analisa as informações e toma decisões baseadas nos dados:
1. Usuário visualiza gráficos gerados
2. Pode aplicar diferentes filtros e regenerar gráficos
3. Pode salvar gráficos importantes como imagens PNG
4. Pode fazer download dos gráficos salvos
5. Sistema mantém histórico de ações via tabela `log`
6. Decisões são tomadas com base nas visualizações e análises apresentadas

**Fluxo de Upload de Arquivos:**
1. Usuário autorizado clica em "Enviar CSV"
2. Modal de upload é exibido
3. Usuário seleciona arquivo CSV do computador
4. Frontend envia arquivo via FormData para `/upload`
5. Backend valida:
   - Extensão do arquivo (.csv)
   - Tamanho do arquivo (se houver limite)
6. Arquivo é salvo na pasta `uploads/`
7. Sistema retorna confirmação de sucesso
8. Lista de arquivos é atualizada automaticamente

**Fluxo de Recuperação de Senha:**
1. Usuário acessa "Esqueci a senha"
2. Informa email cadastrado
3. Sistema gera token único com expiração de 60 minutos
4. Token é salvo na tabela `recuperacao_senha`
5. Email com link de recuperação é enviado
6. Usuário clica no link (contém token)
7. Sistema valida token (existência e expiração)
8. Usuário redefine senha
9. Token é removido após uso bem-sucedido
10. Usuário é redirecionado para login

---

## 5.6 Segurança

**Medidas Implementadas:**
- Hash de senhas com Bcrypt (algoritmo de hash unidirecional)
- Tokens seguros para recuperação de senha (itsdangerous)
- Validação server-side de todos os dados de entrada
- Proteção de rotas com `@login_required`
- Validação de email institucional
- Validação matemática de CPF
- Logs de auditoria de todas as ações importantes
- Proteção contra SQL Injection via ORM
- Expiração automática de tokens
- Sanitização de dados de entrada

---

## 5.7 Estrutura de Arquivos

```
projeto_fmpscGit/
├── app.py                 # Aplicação principal Flask (Backend)
├── config.py              # Configurações (banco, email, secrets)
├── models/                # Modelos de dados (ORM)
│   ├── user.py           # Modelo de Usuário
│   ├── log.py            # Modelo de Log
│   └── recuperacao_senha.py  # Modelo de Token
├── templates/             # Templates HTML (Frontend)
│   ├── login.html
│   ├── cadastro.html
│   ├── index.html        # Dashboard principal
│   └── ...
├── static/                # Arquivos estáticos
│   ├── css/              # Estilos
│   ├── js/               # Scripts JavaScript
│   └── logo.png          # Assets
├── uploads/               # Arquivos CSV enviados
└── saved_charts/         # Gráficos salvos como PNG
```

---

## 5.8 Dependências Principais

**Backend:**
- Flask 3.0.0
- Flask-Login 0.6.3
- Flask-SQLAlchemy 3.1.1
- Flask-Bcrypt 1.0.1
- Flask-Mail 0.9.1
- Pandas 2.1.4
- NumPy 1.26.2
- Plotly 5.18.0
- PyMySQL 1.1.0

**Frontend:**
- Bootstrap 5.3.2 (via CDN)
- Plotly.js 2.32.0 (via CDN)
- Shepherd.js (via CDN)

