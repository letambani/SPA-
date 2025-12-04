# 5.6 Diagrama Simplificado

```
[Frontend]       <-->       [API Flask]     <-->       [Banco de Dados]

    |                                      |                                        |

    |                                      |                                        |

    v                                     v                                       v

  [HTML, CSS]              [Lógica de Negócio]              [MySQL]

   Gráficos               (Processamento de dados)

  Interatividade                  (Filtros, etc.)
```

## Descrição do Diagrama

### [Frontend]
Interface do usuário responsável pela apresentação visual e interação:

- **[HTML, CSS]**: Estruturação e estilização das páginas web
- **Gráficos**: Visualização de dados através de gráficos interativos (Plotly.js)
- **Interatividade**: Elementos interativos como formulários, filtros e navegação

### [API Flask]
Camada de lógica de negócio e processamento:

- **[Lógica de Negócio]**: Regras de negócio, autenticação, validações
- **(Processamento de dados)**: Análise e manipulação de dados CSV com Pandas
- **(Filtros, etc.)**: Aplicação de filtros, agrupamentos e comparações de dados

### [Banco de Dados]
Camada de persistência de dados:

- **[MySQL]**: Sistema de gerenciamento de banco de dados relacional que armazena informações de usuários, logs e tokens

## Fluxo de Comunicação

- **Frontend <--> API Flask**: Comunicação via HTTP/HTTPS com troca de dados em formato JSON
- **API Flask <--> Banco de Dados**: Comunicação via SQLAlchemy ORM para consultas e persistência de dados

## Tecnologias por Camada

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Plotly.js

**API Flask:**
- Flask 3.0.0
- Pandas (processamento de dados)
- Plotly Express (geração de gráficos)

**Banco de Dados:**
- MySQL
- SQLAlchemy ORM

