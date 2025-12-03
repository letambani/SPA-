# Diagrama Simplificado do Sistema SPA

## 5.6 Diagrama Simplificado

```mermaid
graph LR
    subgraph Frontend["[Frontend]"]
        HTML["[HTML, CSS]"]
        Graficos["Gráficos"]
        Interatividade["Interatividade"]
    end
    
    subgraph API["[API Flask]"]
        Logica["[Lógica de Negócio]"]
        Processamento["(Processamento de dados)"]
        Filtros["(Filtros, etc.)"]
    end
    
    subgraph BD["[Banco de Dados]"]
        MySQL["[MySQL]"]
    end
    
    Frontend <--> API
    API <--> BD
    
    Frontend --> HTML
    Frontend --> Graficos
    Frontend --> Interatividade
    
    API --> Logica
    API --> Processamento
    API --> Filtros
    
    BD --> MySQL
    
    style Frontend fill:#E78E74,color:#fff
    style API fill:#0B3353,color:#fff
    style BD fill:#28a745,color:#fff
    style HTML fill:#E78E74,color:#fff
    style Graficos fill:#E78E74,color:#fff
    style Interatividade fill:#E78E74,color:#fff
    style Logica fill:#0B3353,color:#fff
    style Processamento fill:#0B3353,color:#fff
    style Filtros fill:#0B3353,color:#fff
    style MySQL fill:#28a745,color:#fff
```

## Diagrama de Arquitetura em Camadas

```mermaid
graph TB
    subgraph "Camada de Apresentação (Frontend)"
        A[Páginas HTML]
        B[JavaScript/Bootstrap]
        C[Plotly.js]
        D[Formulários]
        E[Filtros Dinâmicos]
        
        A --> B
        B --> C
        B --> D
        B --> E
    end
    
    subgraph "Camada de Comunicação (HTTP/JSON)"
        F[APIs REST]
        G[Endpoints JSON]
        H[Upload de Arquivos]
        
        B --> F
        F --> G
        F --> H
    end
    
    subgraph "Camada de Lógica de Negócio (Backend Flask)"
        I[Rotas Flask]
        J[Autenticação]
        K[Processamento de Dados]
        L[Geração de Gráficos]
        M[Validações]
        
        G --> I
        I --> J
        I --> K
        K --> L
        I --> M
    end
    
    subgraph "Camada de Persistência (Banco de Dados)"
        N[(MySQL)]
        O[Tabela: usuario]
        P[Tabela: log]
        Q[Tabela: recuperacao_senha]
        
        N --> O
        N --> P
        N --> Q
    end
    
    subgraph "Armazenamento de Arquivos"
        R[Pasta: uploads/]
        S[Pasta: saved_charts/]
    end
    
    J --> N
    K --> R
    L --> S
    H --> R
    
    style A fill:#E78E74
    style B fill:#E78E74
    style C fill:#E78E74
    style I fill:#0B3353,color:#fff
    style J fill:#0B3353,color:#fff
    style K fill:#0B3353,color:#fff
    style L fill:#0B3353,color:#fff
    style N fill:#28a745,color:#fff
    style R fill:#ffc107
    style S fill:#ffc107
```

## Fluxo de Autenticação

```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Frontend
    participant B as Backend Flask
    participant DB as MySQL
    
    U->>F: Acessa página de Login
    F->>U: Exibe formulário
    U->>F: Preenche email e senha
    F->>B: POST /login (credenciais)
    B->>DB: Valida usuário
    DB-->>B: Dados do usuário
    B->>B: Verifica senha (Bcrypt)
    alt Credenciais válidas
        B->>DB: Cria log de login
        B->>F: Sessão criada + redirect
        F->>U: Redireciona para Dashboard
    else Credenciais inválidas
        B->>F: Mensagem de erro
        F->>U: Exibe erro
    end
```

## Fluxo de Geração de Gráficos

```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Frontend
    participant API as API /api/grafico
    participant P as Pandas
    participant PL as Plotly
    participant F2 as Frontend Plotly.js
    
    U->>F: Seleciona arquivo CSV
    F->>API: POST /api/columns
    API->>P: Carrega CSV
    P-->>API: Colunas disponíveis
    API-->>F: JSON com colunas
    F->>U: Atualiza seletores
    
    U->>F: Configura gráfico (coluna, tipo, filtros)
    F->>API: POST /api/grafico (parâmetros JSON)
    API->>P: Carrega e filtra CSV
    P-->>API: DataFrame processado
    API->>PL: Gera gráfico Plotly
    PL-->>API: Objeto Plotly JSON
    API-->>F: JSON com dados do gráfico
    F->>F2: Renderiza com Plotly.js
    F2->>U: Exibe gráfico interativo
```

## Diagrama de Componentes do Sistema

```mermaid
graph LR
    subgraph "Frontend"
        A1[Login/Cadastro]
        A2[Dashboard]
        A3[Filtros]
        A4[Visualização]
    end
    
    subgraph "Backend Flask"
        B1[app.py]
        B2[Rotas de Autenticação]
        B3[Rotas de API]
        B4[Processamento]
    end
    
    subgraph "Modelos"
        C1[User Model]
        C2[Log Model]
        C3[RecuperacaoSenha Model]
    end
    
    subgraph "Serviços"
        D1[Flask-Login]
        D2[Flask-Bcrypt]
        D3[Flask-Mail]
        D4[Pandas]
        D5[Plotly Express]
    end
    
    subgraph "Banco de Dados"
        E1[(MySQL)]
    end
    
    A1 --> B2
    A2 --> B3
    A3 --> B3
    A4 --> B3
    
    B2 --> C1
    B3 --> B4
    B4 --> D4
    B4 --> D5
    
    B2 --> D1
    B2 --> D2
    B2 --> D3
    
    C1 --> E1
    C2 --> E1
    C3 --> E1
    
    style A1 fill:#E78E74
    style A2 fill:#E78E74
    style B1 fill:#0B3353,color:#fff
    style E1 fill:#28a745,color:#fff
```

## Fluxo de Upload e Análise de CSV

```mermaid
flowchart TD
    Start([Usuário acessa Dashboard]) --> Auth{Usuário autenticado?}
    Auth -->|Não| Login[Redireciona para Login]
    Auth -->|Sim| Upload[Usuário faz upload CSV]
    
    Upload --> Valida{Arquivo válido?}
    Valida -->|Não| Erro[Exibe erro]
    Valida -->|Sim| Salva[Salva em uploads/]
    
    Salva --> Lista[Lista arquivos disponíveis]
    Lista --> Seleciona[Usuário seleciona arquivo]
    
    Seleciona --> API1[GET /api/columns]
    API1 --> Colunas[Retorna colunas do CSV]
    
    Colunas --> Config[Usuário configura gráfico]
    Config --> Filtros[Usuário aplica filtros]
    
    Filtros --> API2[POST /api/grafico]
    API2 --> Processa[Backend processa com Pandas]
    Processa --> Gera[Gera gráfico com Plotly]
    Gera --> JSON[Retorna JSON do gráfico]
    
    JSON --> Renderiza[Frontend renderiza com Plotly.js]
    Renderiza --> Visualiza[Usuário visualiza gráfico]
    
    Visualiza --> Salvar{Salvar gráfico?}
    Salvar -->|Sim| Save[POST /api/save_chart]
    Save --> PNG[Salva como PNG]
    Salvar -->|Não| Fim([Fim])
    PNG --> Fim
    
    style Start fill:#E78E74
    style Auth fill:#ffc107
    style Processa fill:#0B3353,color:#fff
    style Gera fill:#0B3353,color:#fff
    style Visualiza fill:#28a745,color:#fff
```

## Estrutura de Dados - Modelo Entidade-Relacionamento Simplificado

```mermaid
erDiagram
    USUARIO ||--o{ LOG : "tem"
    USUARIO ||--o{ RECUPERACAO_SENHA : "tem"
    
    USUARIO {
        int id PK
        string nome
        string email UK
        string senha_hash
        string cpf UK
        string cargo
        datetime data_cadastro
        enum status
    }
    
    LOG {
        int id_log PK
        int id_usuario FK
        string acao
        text descricao
        string ip
        datetime data_hora
    }
    
    RECUPERACAO_SENHA {
        int id PK
        int id_usuario FK
        string token UK
        datetime data_criacao
        datetime data_expiracao
    }
```

## Arquitetura de Comunicação Cliente-Servidor

```mermaid
graph TB
    subgraph "Cliente (Browser)"
        C1[HTML/CSS]
        C2[JavaScript]
        C3[Plotly.js]
        C4[Formulários]
    end
    
    subgraph "Servidor Flask"
        S1[Rotas HTTP]
        S2[Autenticação]
        S3[APIs REST]
        S4[Processamento]
    end
    
    subgraph "Dados"
        D1[(MySQL)]
        D2[Arquivos CSV]
        D3[Gráficos PNG]
    end
    
    C1 -->|HTTP Request| S1
    C2 -->|AJAX/JSON| S3
    C4 -->|POST Form| S1
    
    S1 --> S2
    S1 --> S3
    S3 --> S4
    
    S2 -->|Query| D1
    S4 -->|Read| D2
    S4 -->|Write| D3
    
    S3 -->|JSON Response| C2
    S1 -->|HTML Response| C1
    C2 -->|Render| C3
    
    style C1 fill:#E78E74
    style C2 fill:#E78E74
    style S1 fill:#0B3353,color:#fff
    style S3 fill:#0B3353,color:#fff
    style D1 fill:#28a745,color:#fff
```

## Legenda

- **Laranja (#E78E74)**: Componentes Frontend
- **Azul Escuro (#0B3353)**: Componentes Backend
- **Verde (#28a745)**: Banco de Dados
- **Amarelo (#ffc107)**: Armazenamento de Arquivos

---

## Notas sobre o Diagrama

1. **Camada de Apresentação**: Responsável pela interface do usuário e interações visuais
2. **Camada de Comunicação**: Gerencia a troca de dados via HTTP/JSON entre frontend e backend
3. **Camada de Lógica de Negócio**: Processa requisições, valida dados e gera gráficos
4. **Camada de Persistência**: Armazena dados de usuários, logs e tokens
5. **Armazenamento de Arquivos**: Gerencia arquivos CSV e gráficos salvos

O sistema segue uma arquitetura em camadas (layered architecture) que separa responsabilidades e facilita manutenção e escalabilidade.

