# 🚀 Guia para Publicar no GitHub

## Passo 1: Criar Repositório no GitHub

1. Acesse [GitHub.com](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito
3. Selecione **"New repository"**
4. Preencha:
   - **Repository name**: `projeto-fmpsc-spa` (ou outro nome de sua preferência)
   - **Description**: "Sistema de Perfil Discente - FMPSC"
   - **Visibility**: Escolha Público ou Privado
   - **NÃO marque** "Initialize with README" (já temos um)
5. Clique em **"Create repository"**

## Passo 2: Conectar e Fazer Push

Após criar o repositório, o GitHub mostrará comandos. Execute estes comandos no terminal:

```bash
cd /Users/leticiatambani/Desktop/projeto_fmpscGit

# Adicionar o repositório remoto (substitua USERNAME pelo seu usuário do GitHub)
git remote add origin https://github.com/USERNAME/projeto-fmpsc-spa.git

# Renomear branch para main (se necessário)
git branch -M main

# Fazer push do código
git push -u origin main
```

## Passo 3: Adicionar Protótipo HTML (Opcional)

Se você tiver o arquivo HTML do protótipo de alta fidelidade:

1. Coloque o arquivo na pasta `prototipo/`
2. Execute:
```bash
git add prototipo/
git commit -m "Adiciona protótipo de alta fidelidade"
git push
```

## ✅ Verificação

Após o push, acesse seu repositório no GitHub e verifique se todos os arquivos foram enviados corretamente.

## 📝 Notas

- O arquivo `config.py` contém informações sensíveis e está no `.gitignore` para segurança
- Certifique-se de não fazer commit de senhas ou tokens
- Os arquivos CSV em `uploads/` não serão commitados (apenas a estrutura)

