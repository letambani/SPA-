# 📊 Modelos de Visualizações Dinâmicas

Este documento descreve os modelos de gráficos dinâmicos, mapas de calor e mapas geográficos disponíveis no sistema SPA FMPSC.

## 🎨 Visualizações Disponíveis

### 1. **Gráfico de Barras - Distribuição por Curso**
- **Tipo**: Gráfico de barras vertical
- **Descrição**: Mostra a quantidade de alunos por curso
- **Cores**: Escala de azuis (Blues)
- **Interatividade**: Hover para ver valores exatos, zoom, pan

### 2. **Gráfico de Pizza - Distribuição por Gênero**
- **Tipo**: Gráfico de pizza (pie chart)
- **Descrição**: Mostra a proporção de alunos por gênero
- **Cores**: Paleta qualitativa Set3
- **Interatividade**: Clique para destacar segmentos, hover para detalhes

### 3. **Gráfico de Barras - Faixa Etária**
- **Tipo**: Gráfico de barras vertical
- **Descrição**: Distribuição dos alunos por faixa etária
- **Cores**: Escala de laranjas (Oranges)
- **Interatividade**: Ordenação automática por idade

### 4. **Heatmap - Curso vs Cidade**
- **Tipo**: Mapa de calor (heatmap)
- **Descrição**: Matriz mostrando a distribuição de alunos por curso e cidade
- **Cores**: Escala YlOrRd (amarelo-laranja-vermelho)
- **Interatividade**: Hover para ver valores, zoom na matriz

### 5. **Gráfico de Barras Horizontais - Cor/Raça**
- **Tipo**: Gráfico de barras horizontal
- **Descrição**: Distribuição de alunos por cor/raça
- **Cores**: Escala Viridis
- **Interatividade**: Fácil leitura de categorias

### 6. **Gráfico de Barras - Meio de Divulgação**
- **Tipo**: Gráfico de barras vertical
- **Descrição**: Como os alunos conheceram a FMP
- **Cores**: Escala de roxos (Purples)
- **Interatividade**: Rotação de labels para melhor visualização

### 7. **Gráfico de Barras - Situação de Trabalho**
- **Tipo**: Gráfico de barras vertical
- **Descrição**: Quantidade de alunos que trabalham ou não
- **Cores**: Escala de verdes (Greens)
- **Interatividade**: Comparação visual simples

### 8. **Gráfico de Barras - Faixa de Renda**
- **Tipo**: Gráfico de barras vertical
- **Descrição**: Distribuição por faixa de renda familiar
- **Cores**: Escala de vermelhos (Reds)
- **Interatividade**: Ordenação lógica por faixa de renda

### 9. **Heatmap de Correlação**
- **Tipo**: Mapa de calor de correlação
- **Descrição**: Correlação entre variáveis numéricas do dataset
- **Cores**: Escala RdBu (vermelho-azul) - valores positivos em azul, negativos em vermelho
- **Interatividade**: Identifica relações entre variáveis numéricas

### 10. **Mapa Geográfico Interativo**
- **Tipo**: Mapa interativo com marcadores proporcionais
- **Descrição**: Distribuição geográfica dos alunos por cidade
- **Características**:
  - Marcadores circulares proporcionais à quantidade
  - Cores variando de laranja (mais alunos) para azul (menos alunos)
  - Tooltips informativos
  - Zoom e pan automático
  - Estatísticas resumidas (Total de Alunos, Cidades, Maior Concentração)

## 🚀 Como Usar

### Método 1: Visualizações Completas (Recomendado)
1. Selecione um arquivo CSV no dropdown "Arquivo base"
2. Clique no botão **"🎨 Gerar Todas as Visualizações"** no card azul
3. O sistema gerará automaticamente todos os gráficos disponíveis baseados nos dados do CSV

### Método 2: Gráficos Individuais
1. Selecione um arquivo CSV
2. Escolha a coluna principal
3. Selecione o tipo de gráfico (barras, pizza, linha, histograma)
4. Aplique filtros opcionais
5. Clique em "Gerar Gráfico"

### Método 3: Mapa Geográfico
1. Selecione um arquivo CSV
2. Clique no botão **"🗺️ Mapa Geográfico"** no card de resultados
3. O mapa será gerado automaticamente com base na coluna de município/cidade

## 📋 Requisitos dos Dados

O sistema detecta automaticamente as colunas relevantes procurando por palavras-chave:

- **Curso**: "curso", "Curso"
- **Gênero**: "gênero", "genero", "identifica"
- **Idade**: "faixa etária", "idade"
- **Cidade**: "município", "cidade", "residência"
- **Cor/Raça**: "cor", "raça"
- **Divulgação**: "divulgação", "conheceu"
- **Trabalho**: "trabalhando", "trabalha"
- **Renda**: "renda"

## 🎯 Tecnologias Utilizadas

- **Plotly.js**: Gráficos interativos
- **Plotly Express (Python)**: Geração de gráficos no backend
- **Leaflet.js**: Mapas geográficos interativos
- **Pandas**: Processamento de dados
- **NumPy**: Cálculos numéricos e correlações

## 💡 Dicas

1. **Para melhor visualização**: Use o botão "Gerar Todas as Visualizações" para ter uma visão completa dos dados
2. **Download**: Todos os gráficos podem ser baixados como PNG clicando no botão 📥
3. **Interatividade**: Passe o mouse sobre os gráficos para ver valores detalhados
4. **Zoom**: Use a ferramenta de zoom nos gráficos Plotly para análises detalhadas
5. **Filtros**: Aplique filtros antes de gerar gráficos individuais para análises específicas

## 📊 Exemplos de Uso

### Análise de Perfil Discente
Use as visualizações completas para ter uma visão geral do perfil dos alunos:
- Distribuição por curso
- Perfil demográfico (gênero, idade, cor/raça)
- Situação socioeconômica (renda, trabalho)
- Origem geográfica (mapa)

### Análise de Divulgação
Use o gráfico de "Meio de Divulgação" para entender como os alunos conheceram a instituição

### Análise Geográfica
Use o mapa geográfico para identificar:
- Cidades com maior concentração de alunos
- Necessidade de transporte ou apoio regional
- Expansão geográfica do público

### Análise de Correlação
Use o heatmap de correlação para identificar relações entre variáveis numéricas

## 🔄 Atualizações Futuras

- Gráficos de linha temporal (se houver dados de data)
- Gráficos de dispersão para análise multivariada
- Clusters no mapa geográfico para melhor visualização
- Exportação em PDF de todas as visualizações
- Comparação temporal entre diferentes períodos

