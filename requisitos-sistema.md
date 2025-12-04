# 3. Requisitos do Sistema

## 3.1 Requisitos Funcionais

### RF-01

**Identificador:** RF-01

**Prioridade:** ALTA

**Nome:** Cadastro

**Data de Criação:** 2024

**Autor:** Equipe de Desenvolvimento

**Descrição:**

A aplicação deve conter uma página de cadastro com verificação do email institucional (@coordenador e presidente@fmpsc.edu.br, coordenacao.ads@fmpsc.edu.br, coordenacao.adm@fmpsc.edu.br, coordenacao.ped@fmpsc.edu.br, coordenacao.pgr@fmpsc.edu.br, coordenacao.coper@fmpsc.edu.br, soa@fmpsc.edu.br, etc) e senha criptografada. Senha com no mínimo 8 caracteres. O sistema deve validar nome, e-mail institucional, cargo, senha e confirmação de senha. Após o cadastro, será enviado um token para o email cadastrado e o usuário será direcionado para página de validação.

---

### RF-02

**Identificador:** RF-02

**Prioridade:** ALTA

**Nome:** Login

**Data de Criação:** 2024

**Autor:** Equipe de Desenvolvimento

**Descrição:**

A aplicação deve ter uma página específica para login (index/home) e a senha deve ser criptografada. O usuário deve informar email e senha para verificação de acesso. Após autenticação bem-sucedida, o usuário é direcionado para página de visualização dos gráficos. O sistema deve permitir recuperação de senha através da opção "esqueci a senha".

---

### RF-03

**Identificador:** RF-03

**Prioridade:** ALTA

**Nome:** Token

**Data de Criação:** 2024

**Autor:** Equipe de Desenvolvimento

**Descrição:**

A aplicação deve enviar um código de confirmação por e-mail. Após preencher o cadastro, o usuário é redirecionado para uma página onde deve colocar o código que foi enviado para validação do e-mail, após essa confirmação, o cadastro é concluído. Essa etapa também acontece na validação de troca de senha. O token deve ter validade temporal e ser único para cada solicitação.

---

### RF-04

**Identificador:** RF-04

**Prioridade:** ALTA

**Nome:** Alteração de senha

**Data de Criação:** 2024

**Autor:** Equipe de Desenvolvimento

**Descrição:**

A aplicação deve permitir a alteração de senha. Após clicar em "Esqueci a senha", o usuário poderá fazer o processo de trocar de senha. O sistema deve solicitar e-mail, nova senha e confirmação de nova senha. Após enviar, será encaminhado para validação do "Token" enviado pelo e-mail. O sistema deve validar se o e-mail está cadastrado e verificar se o token é válido e não expirou.

---

### RF-05

**Identificador:** RF-05

**Prioridade:** ALTA

**Nome:** Gráfico interativo

**Data de Criação:** 2024

**Autor:** Equipe de Desenvolvimento

**Descrição:**

A aplicação deve conter pelo menos 1 gráfico interativo. O sistema deve permitir filtros, dando a possibilidade da pessoa além de ver a exibição geral dos gráficos (de todos os cursos), ela poder selecionar os cursos e ver os detalhes de cada curso separadamente, além de poder selecionar o tipo de gráfico que deseja exibir (barras, pizza, linha, histograma). O usuário deve poder visualizar os dados de forma dinâmica e personalizada após estar logado.

---

### RF-06

**Identificador:** RF-06

**Prioridade:** ALTA

**Nome:** Download de gráfico

**Data de Criação:** 2024

**Autor:** Equipe de Desenvolvimento

**Descrição:**

A aplicação deve permitir o download dos gráficos. Deve haver um botão para download. Após escolher o tipo de exibição dos gráficos e os dados, o usuário tem a opção de baixar uma imagem do gráfico para salvá-la. O sistema deve validar se há um gráfico gerado antes de permitir o download, exibindo mensagem caso não haja gráfico disponível.

---

### RF-07

**Identificador:** RF-07

**Prioridade:** ALTA

**Nome:** Salvar gráfico

**Data de Criação:** 2024

**Autor:** Equipe de Desenvolvimento

**Descrição:**

A aplicação deve permitir salvar gráficos. Deve haver um botão para salvar. Após escolher o tipo de exibição dos gráficos e os dados, o usuário tem a opção de salvar o gráfico selecionado. Quando fizer isso, o gráfico ficará estático na parte inferior da tela, e todos os gráficos salvos subsequentes terão o mesmo comportamento. O sistema deve validar se há um gráfico gerado antes de permitir o salvamento.

---

## 3.2 Requisitos Não Funcionais

### RNF-01

**Identificador:** RNF-01

**Prioridade:** ALTA

**Nome:** Usabilidade

**Data de Criação:** 2024

**Autor:** Equipe de Desenvolvimento

**Descrição:**

A aplicação deve conter um layout intuitivo. A aplicação deve apresentar uma interface clara, de fácil navegação e entendimento, permitindo que o usuário localize informações e realize ações sem dificuldades. O usuário deve conseguir navegar entre as telas, identificando menus, botões e elementos visuais de forma simples e objetiva. Caso algum elemento da interface apresente falhas, o sistema deve exibir uma mensagem de erro ou alerta apropriada.

---

### RNF-02

**Identificador:** RNF-02

**Prioridade:** ALTA

**Nome:** Identidade Visual

**Data de Criação:** 2024

**Autor:** Equipe de Desenvolvimento

**Descrição:**

A aplicação deve ser padronizada de acordo com a identidade visual do logo. As cores padrão são: #FFFFFF - Branco (255,255,255), #E78E74 - Laranja (231, 142, 116), #0B3353 - Azul (11,51,83). A aplicação deve exibir uniformidade visual em todas as telas e componentes, mantendo consistência nas cores, fontes e logotipo definidos no padrão da identidade visual.

---

### RNF-03

**Identificador:** RNF-03

**Prioridade:** ALTA

**Nome:** Compatibilidade

**Data de Criação:** 2024

**Autor:** Equipe de Desenvolvimento

**Descrição:**

O sistema deve ser capaz de funcionar nos principais navegadores (Chrome, Edge, Mozilla) e sistemas operacionais (Linux, Windows, iOS). A aplicação deve executar corretamente suas funcionalidades e manter o mesmo comportamento em diferentes plataformas e navegadores. O sistema deve adaptar a interface conforme o dispositivo e navegador. Caso o acesso ocorra por meio de um navegador desatualizado ou não compatível, o sistema deve exibir uma mensagem informando a limitação de suporte.

---

### RNF-04

**Identificador:** RNF-04

**Prioridade:** ALTA

**Nome:** Desempenho

**Data de Criação:** 2024

**Autor:** Equipe de Desenvolvimento

**Descrição:**

A aplicação deve ter um bom desempenho. O sistema deve ser capaz de processar e responder às consultas em até 5 segundos. O sistema deve retornar o resultado solicitado dentro do tempo especificado para operações como consulta, filtro, geração de gráfico ou carregamento de dados. Caso o sistema identifique lentidão, sobrecarga ou falha durante o processamento, ele deve exibir uma mensagem informando a ocorrência do problema e oferecer ao usuário a opção de tentar novamente.

---

### RNF-05

**Identificador:** RNF-05

**Prioridade:** ALTA

**Nome:** Segurança

**Data de Criação:** 2024

**Autor:** Equipe de Desenvolvimento

**Descrição:**

A aplicação deve garantir a proteção dos dados dos usuários por meio de autenticação segura, criptografia de senhas e controle de acesso às informações sensíveis. O sistema deve assegurar a integridade e confidencialidade das informações, impedindo acessos não autorizados. O usuário deve estar cadastrado e autenticado para acessar recursos restritos. O sistema deve autenticar e validar credenciais de forma segura, negando acesso e exibindo mensagem informativa caso as credenciais sejam inválidas.

