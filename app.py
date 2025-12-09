# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
import re
import numpy as np
import pandas as pd
import plotly.express as px

from config import Config
from models.user import db, bcrypt, User
from models.log import Log
from models.recuperacao_senha import RecuperacaoSenha

# ---------------- app / config ----------------
app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_ECHO'] = True

# ---------------- extensões ----------------
db.init_app(app)
bcrypt.init_app(app)
mail = Mail(app)

# ---------------- login ----------------
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- utilitários ----------------
def enviar_email_boas_vindas(email, nome):
    try:
        msg = Message(subject="🎉 Bem-vindo(a) ao SPA - FMPSC!",
                      recipients=[email])
        msg.html = f"""
        <div style="font-family:Arial,sans-serif;color:#0B3353;">
            <h2>Olá, {nome}!</h2>
            <p>Seu cadastro no <strong>SPA - Sistema de Perfil Discente</strong> foi realizado com sucesso!</p>
            <p>Agora você pode acessar sua conta e começar a usar a plataforma.</p>
            <p style="margin-top:20px;">💡 Caso não tenha sido você, ignore este e-mail.</p>
            <br>
            <p>Atenciosamente,<br><strong>Equipe FMPSC</strong></p>
        </div>
        """
        mail.send(msg)
        app.logger.info("E-mail de boas-vindas enviado para %s", email)
    except Exception as e:
        app.logger.exception("Erro ao enviar e-mail de boas-vindas: %s", e)

# itsdangerous serializer (para tokens)
def _serializer():
    return URLSafeTimedSerializer(app.config['SECRET_KEY'])

# ---------------- ROTAS ----------------

@app.route('/')
def home():
    return redirect(url_for('login'))

# ----- LOGIN -----
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        senha = request.form['senha']
        usuario = User.query.filter_by(email=email).first()

        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)

            log = Log(id_usuario=usuario.id, acao='Login',
                      descricao='Usuário fez login no sistema', ip=request.remote_addr)
            db.session.add(log)
            db.session.commit()

            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('analises'))
        else:
            flash('E-mail ou senha incorretos.', 'danger')

    return render_template('login.html')

# ----- CADASTRO -----
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        cpf = request.form['cpf'].strip()
        email = request.form['email'].strip().lower()
        cargo = request.form['cargo']
        senha = request.form['senha']
        confirmar = request.form['confirmar']

        padrao_email = re.compile(r'.+@aluno\.fmpsc\.edu\.br$', re.IGNORECASE)
        padrao_cpf = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')

        if not padrao_email.match(email):
            flash('Use um e-mail institucional válido (@fmpsc.edu.br).', 'warning')
            return render_template('cadastro.html')

        # validação CPF matemática (server-side)
        def validar_cpf(cpf_val):
            cpf_n = re.sub(r'[^0-9]', '', cpf_val)
            if len(cpf_n) != 11 or cpf_n == cpf_n[0]*11:
                return False
            soma = sum(int(cpf_n[i]) * (10 - i) for i in range(9))
            resto = (soma * 10) % 11
            if resto == 10: resto = 0
            if resto != int(cpf_n[9]): return False
            soma = sum(int(cpf_n[i]) * (11 - i) for i in range(10))
            resto = (soma * 10) % 11
            if resto == 10: resto = 0
            return resto == int(cpf_n[10])

        if not padrao_cpf.match(cpf):
            flash('Digite o CPF no formato 000.000.000-00.', 'warning')
            return render_template('cadastro.html')

        if not validar_cpf(cpf):
            flash('CPF inválido. Verifique e tente novamente.', 'warning')
            return render_template('cadastro.html')

        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'info')
            return render_template('cadastro.html')

        if User.query.filter_by(cpf=cpf).first():
            flash('CPF já cadastrado.', 'info')
            return render_template('cadastro.html')

        if len(senha) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.', 'warning')
            return render_template('cadastro.html')

        if senha != confirmar:
            flash('As senhas não coincidem.', 'danger')
            return render_template('cadastro.html')

        try:
            novo_usuario = User(nome=nome, email=email, cargo=cargo, cpf=cpf)
            novo_usuario.senha = senha
            db.session.add(novo_usuario)
            db.session.commit()

            log = Log(id_usuario=novo_usuario.id, acao='Cadastro',
                      descricao='Novo usuário cadastrado', ip=request.remote_addr)
            db.session.add(log)
            db.session.commit()

            enviar_email_boas_vindas(email, nome)
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            app.logger.exception("Erro ao cadastrar usuário: %s", e)
            flash('Erro ao cadastrar usuário. Tente novamente.', 'danger')
            return render_template('cadastro.html')

    return render_template('cadastro.html')

# ----- DASHBOARD -----
# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html', nome=current_user.nome)

# ----- LOGOUT -----
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('login'))

# ---------------- RECUPERAR SENHA (envia link por e-mail e registra token) ----------------
@app.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        usuario = User.query.filter_by(email=email).first()

        if not usuario:
            flash('E-mail não encontrado.', 'warning')
            return redirect(url_for('login'))

        # gera token itsdangerous
        s = _serializer()
        token = s.dumps(usuario.email, salt='recuperar-senha')

        # grava token na tabela de recuperacao (opcional p/ auditoria/expiração)
        agora = datetime.utcnow()
        expira = agora + timedelta(minutes=60)
        rec = RecuperacaoSenha(id_usuario=usuario.id, token=token,
                               data_criacao=agora, data_expiracao=expira)
        db.session.add(rec)
        db.session.commit()

        link = url_for('reset_senha', token=token, _external=True)

        # envia e-mail
        msg = Message(subject="Recuperação de Senha - FMPSC SPA",
                      recipients=[usuario.email])
        msg.html = (f"<p>Olá {usuario.nome},</p>"
                    f"<p>Recebemos uma solicitação para redefinir sua senha. Clique no link abaixo:</p>"
                    f"<p><a href='{link}'>{link}</a></p>"
                    f"<p>O link expira em 60 minutos.</p>")
        try:
            mail.send(msg)
            # log da solicitação
            log = Log(id_usuario=usuario.id, acao='Solicitou recuperação',
                      descricao='Solicitação de recuperação de senha (envio de token)', ip=request.remote_addr)
            db.session.add(log)
            db.session.commit()

            flash('Um e-mail com instruções foi enviado.', 'success')
        except Exception as e:
            app.logger.exception("Erro ao enviar e-mail de recuperação: %s", e)
            flash('Erro ao enviar e-mail. Tente novamente mais tarde.', 'danger')

        return redirect(url_for('login'))

    return render_template('recuperar_senha.html')

# ---------------- REDEFINIR SENHA (usa token) ----------------
@app.route('/reset_senha/<token>', methods=['GET', 'POST'])
def reset_senha(token):
    # primeiro valida token com itsdangerous (tempo)
    s = _serializer()
    try:
        email = s.loads(token, salt='recuperar-senha', max_age=3600)
    except Exception:
        flash("Link inválido ou expirado.", "danger")
        return redirect(url_for('recuperar_senha'))

    # também valida existência no DB (p/ garantir token válido)
    rec = RecuperacaoSenha.query.filter_by(token=token).first()
    if not rec or rec.data_expiracao < datetime.utcnow():
        flash("Token inválido ou expirado.", "danger")
        return redirect(url_for('recuperar_senha'))

    if request.method == 'POST':
        nova_senha = request.form.get('senha')
        confirmar = request.form.get('confirmar_senha')


        if not nova_senha or not confirmar:
            flash('Preencha ambos os campos de senha.', 'warning')
            return render_template('reset_senha.html')

        if nova_senha != confirmar:
            flash('As senhas não coincidem.', 'danger')
            return render_template('reset_senha.html')

        if len(nova_senha) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.', 'warning')
            return render_template('reset_senha.html')


        usuario = User.query.filter_by(email=email).first()
        if not usuario:
            flash('Usuário não encontrado.', 'danger')
            return redirect(url_for('recuperar_senha'))

        # 🔒 atualiza com hash via setter do modelo
        usuario.senha = nova_senha
        db.session.add(usuario)

        # log
        novo_log = Log(
            id_usuario=usuario.id,
            acao="Recuperação de Senha",
            descricao="Usuário redefiniu a senha via link",
            ip=request.remote_addr,
            data_hora=datetime.utcnow()
        )
        db.session.add(novo_log)

        # remove token usado
        db.session.delete(rec)
        db.session.commit()

        flash("Senha redefinida com sucesso! Você já pode fazer login.", "success")
        return redirect(url_for('login'))


    return render_template('reset_senha.html')

# ------------------------------------------------------
# 🔵 MÓDULO DE GRÁFICOS / CSV / ABA DE ANÁLISES
# ------------------------------------------------------
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json
import base64
import uuid
from flask import jsonify, send_file
import io

# pastas
UPLOADS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
SAVED_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'saved_charts')
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(SAVED_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        return jsonify(success=False, error="Nenhum arquivo enviado")

    file = request.files['file']

    if file.filename == "":
        return jsonify(success=False, error="Arquivo inválido")

    if not file.filename.lower().endswith(".csv"):
        return jsonify(success=False, error="Envie apenas CSV")

    save_path = os.path.join(UPLOADS_DIR, file.filename)
    file.save(save_path)

    return jsonify(success=True)



def list_uploaded_files():
    """Lista CSV na pasta uploads/"""
    return [f for f in os.listdir(UPLOADS_DIR) if f.lower().endswith('.csv')]


def load_csv(filename):
    """Carrega CSV especificado"""
    path = os.path.join(UPLOADS_DIR, filename)
    return pd.read_csv(path)


def abreviar_curso(nome_curso):
    """
    Abrevia nomes de cursos para exibição nos gráficos.
    Retorna a abreviação correspondente ou o nome original se não houver mapeamento.
    """
    if pd.isna(nome_curso):
        return nome_curso
    
    nome_str = str(nome_curso).strip()
    
    # Mapeamento de nomes completos para abreviações
    mapeamento = {
        # Análise e Desenvolvimento de Sistemas
        'tecnólogo em análise e desenvolvimento de sistemas': 'ADS',
        'análise e desenvolvimento de sistemas': 'ADS',
        'ads': 'ADS',
        'análise e desenvolvimento': 'ADS',
        'analise e desenvolvimento de sistemas': 'ADS',
        
        # Administração / Gestão Pública
        'tecnólogo em gestão pública': 'ADM',
        'gestão pública': 'ADM',
        'administração': 'ADM',
        'adm': 'ADM',
        'gestao publica': 'ADM',
        
        # Gestão de Recursos Humanos
        'tecnólogo em gestão de recursos humanos': 'GRH',
        'gestão de recursos humanos': 'GRH',
        'grh': 'GRH',
        'gestao de recursos humanos': 'GRH',
        'recursos humanos': 'GRH',
        
        # Pedagogia
        'licenciatura em pedagogia': 'Pedagogia',
        'pedagogia': 'Pedagogia',
    }
    
    # Busca case-insensitive
    nome_lower = nome_str.lower()
    for chave, abreviacao in mapeamento.items():
        if chave in nome_lower or nome_lower in chave:
            return abreviacao
    
    # Se não encontrou, retorna o nome original
    return nome_str


def aplicar_abreviacao_cursos(df, coluna_curso):
    """
    Aplica abreviação de cursos em uma coluna específica do DataFrame.
    Retorna o DataFrame modificado.
    """
    if coluna_curso and coluna_curso in df.columns:
        df = df.copy()
        df[coluna_curso] = df[coluna_curso].apply(abreviar_curso)
    return df


# ---------------- INDEX DOS GRÁFICOS ----------------
@app.route('/analises')
@login_required
def analises():
    files = list_uploaded_files()
    return render_template('index.html', files=files)


# ---------------- API: COLUNAS ----------------
@app.route('/api/columns', methods=['POST'])
@login_required
def api_columns():
    data = request.get_json()
    filename = data.get("filename")

    if not filename:
        return jsonify(error="Nenhum arquivo selecionado"), 400

    try:
        df = load_csv(filename)
    except Exception as e:
        return jsonify(error=str(e)), 400

    cols = []
    for col in df.columns:
        col_data = df[col]
        cols.append({
            "name": col,
            "is_numeric": bool(pd.api.types.is_numeric_dtype(col_data)),
            "unique_values_count": int(col_data.nunique(dropna=True)),
            "sample_values": col_data.dropna().astype(str).unique()[:10].tolist()
        })

    return jsonify(columns=cols)


# ---------------- API: GERAR GRÁFICO ----------------
@app.route('/api/grafico', methods=['POST'])
@login_required
def api_grafico():
    payload = request.get_json()
    filename = payload.get("filename")
    compare_with = payload.get("compare_with")  # optional
    coluna = payload.get("coluna")
    tipo = payload.get("tipo", "bar")
    filtros = payload.get("filtros", {}) or {}
    groupby = payload.get("groupby")  # optional

    if not filename or not coluna:
        return jsonify(error="Informe 'filename' e 'coluna'."), 400

    # carrega base
    try:
        df1 = load_csv(filename)
    except Exception as e:
        return jsonify(error=f"Erro ao abrir arquivo base: {e}"), 400

    # checa existência das colunas na base
    if coluna not in df1.columns:
        return jsonify(error=f"A coluna '{coluna}' não existe em {filename}"), 400
    if groupby and (groupby not in df1.columns):
        return jsonify(error=f"O agrupamento '{groupby}' não existe em {filename}"), 400

    # aplica filtros no df1 (assume filtros: {col: [vals]})
    def apply_filters(df, filtros):
        df = df.copy()
        for fcol, vals in (filtros or {}).items():
            if not vals: continue
            if fcol not in df.columns:
                # ignora filtros que não existem
                continue
            df[fcol] = df[fcol].astype(str)
            vals = [str(v) for v in vals]
            df = df[df[fcol].isin(vals)]
        return df

    df1 = apply_filters(df1, filtros)

    # Aplica abreviação de cursos se a coluna for de curso
    if 'curso' in coluna.lower():
        df1 = aplicar_abreviacao_cursos(df1, coluna)
    
    # função auxiliar: gerar figura de contagem por 'coluna' a partir de um dataframe
    def fig_from_df(df, title_suffix=""):
        # trata NA como string 'N/A' para exibir
        ser = df[coluna].fillna("N/A").astype(str)
        if tipo == "histogram":
            fig = px.histogram(df, x=coluna, title=f"{coluna} {title_suffix}")
        else:
            counts = ser.value_counts().reset_index()
            counts.columns = ["categoria", "total"]
            # ordenar por total decrescente
            counts = counts.sort_values("total", ascending=False)
            if tipo == "bar":
                fig = px.bar(counts, x="categoria", y="total", title=f"{coluna} {title_suffix}")
            elif tipo == "pie":
                fig = px.pie(counts, names="categoria", values="total", title=f"{coluna} {title_suffix}")
            elif tipo == "line":
                fig = px.line(counts, x="categoria", y="total", title=f"{coluna} {title_suffix}")
            else:
                # fallback
                fig = px.bar(counts, x="categoria", y="total", title=f"{coluna} {title_suffix}")
        return fig

    # conversor safe (numpy -> list) para JSON serializável
    def convert(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        if isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [convert(v) for v in obj]
        return obj

    resultados = []

    # ---------- se groupby informado => percorrer grupos (base) ----------
    grupos = [None]  # None significa "todo o arquivo"
    if groupby:
        # usar valores do arquivo base para fazer os grupos
        grupos = df1[groupby].dropna().astype(str).unique().tolist()

    # função para extrair contagens por categoria de uma dataframe (retorna dict categoria->count)
    def counts_dict(df):
        s = df[coluna].fillna("N/A").astype(str)
        vc = s.value_counts()
        # converter índice e valores para dict
        return {str(k): int(v) for k,v in vc.items()}

    # ---------- carrega arquivo de comparação (se existir) e valida colunas ----------
    df2 = None
    if compare_with:
        try:
            df2 = load_csv(compare_with)
        except Exception as e:
            return jsonify(error=f"Erro ao abrir arquivo de comparação: {e}"), 400
        if coluna not in df2.columns:
            return jsonify(error=f"A coluna '{coluna}' não existe em {compare_with}"), 400
        if groupby and (groupby not in df2.columns):
            return jsonify(error=f"O agrupamento '{groupby}' não existe em {compare_with}"), 400
        # aplicar mesmos filtros (aplicados ao df1) também ao df2
        df2 = apply_filters(df2, filtros)
        # Aplica abreviação de cursos se a coluna for de curso
        if 'curso' in coluna.lower():
            df2 = aplicar_abreviacao_cursos(df2, coluna)

    # ---------- para cada grupo (ou geral) gerar gráficos e comparar ----------
    for g in grupos:
        # subset
        if g is None:
            sub1 = df1
            sub2 = df2 if df2 is not None else None
            title_post = "(GERAL)"
        else:
            sub1 = df1[df1[groupby].astype(str) == str(g)]
            sub2 = df2[df2[groupby].astype(str) == str(g)] if df2 is not None else None
            title_post = f"({groupby}: {g})"

        # gráfico do arquivo base
        fig1 = fig_from_df(sub1, title_suffix=f"- Base {title_post}")
        resultados.append({"title": f"Base — {filename} {title_post}", "fig": convert(fig1.to_plotly_json())})

        # gráfico do comparador (se houver)
        if sub2 is not None:
            fig2 = fig_from_df(sub2, title_suffix=f"- Comparador {title_post}")
            resultados.append({"title": f"Comparador — {compare_with} {title_post}", "fig": convert(fig2.to_plotly_json())})

            # construir terceiro gráfico: % diferença por categoria (comparador vs base)
            c1 = counts_dict(sub1)
            c2 = counts_dict(sub2)

            # criar lista de todas as categorias presentes em qualquer um
            categorias = sorted(set(list(c1.keys()) + list(c2.keys())), key=lambda x: (-max(c1.get(x,0), c2.get(x,0)), x))

            pct_changes = []
            for cat in categorias:
                v1 = c1.get(cat, 0)
                v2 = c2.get(cat, 0)
                # regra para dividir por zero:
                if v1 == 0:
                    if v2 == 0:
                        pct = 0.0
                    else:
                        pct = 100.0  # novo valor (interpretação: +100%)
                else:
                    pct = ( (v2 - v1) / v1 ) * 100.0
                pct_changes.append({"categoria": cat, "base": v1, "comp": v2, "pct": round(pct, 2)})

            # criar dataframe para plot
            df_diff = pd.DataFrame(pct_changes)

            # gráfico de barras para % (com cores para + / -)
            # usamos Plotly para deixar visual agradável
            fig_diff = px.bar(df_diff, x="categoria", y="pct", title=f"Variação % (Comparador vs Base) {title_post}")
            # ajustar layout: linha zero visível
            fig_diff.update_layout(yaxis=dict(title="Variação (%)", zeroline=True, zerolinewidth=2, zerolinecolor='LightGrey'), xaxis_tickangle=-45)

            # adicionar anotações com base/comp (opcional)
            resultados.append({"title": f"Variação % — {compare_with} vs {filename} {title_post}", "fig": convert(fig_diff.to_plotly_json())})

    return jsonify({"graficos": resultados})


# ---------------- API: SALVAR GRÁFICO ----------------
@app.route('/api/save_chart', methods=['POST'])
@login_required
def api_save_chart():
    data = request.get_json()
    data_url = data.get("data_url")

    header, encoded = data_url.split(",", 1)
    binary = base64.b64decode(encoded)

    fname = f"chart_{uuid.uuid4().hex[:8]}.png"
    path = os.path.join(SAVED_DIR, fname)

    with open(path, "wb") as f:
        f.write(binary)

    return jsonify(saved=True, file=fname)


# ---------------- API: DOWNLOAD ----------------
@app.route('/download_chart/<filename>')
@login_required
def download_chart(filename):
    path = os.path.join(SAVED_DIR, filename)

    if not os.path.exists(path):
        flash("Arquivo não encontrado.", "danger")
        return redirect(url_for('analises'))

    return send_file(path, as_attachment=True)

# ---------------- API: MAPA GEOGRÁFICO ----------------
@app.route('/api/mapa_geografico', methods=['POST'])
@login_required
def api_mapa_geografico():
    """Processa CSV e retorna dados geográficos por cidade"""
    data = request.get_json()
    filename = data.get("filename")
    
    if not filename:
        return jsonify(error="Nenhum arquivo selecionado"), 400
    
    try:
        df = load_csv(filename)
    except Exception as e:
        return jsonify(error=f"Erro ao abrir arquivo: {e}"), 400
    
    # Mapeia nomes de colunas possíveis para cidade
    coluna_cidade = None
    possiveis_colunas = [
        'Qual seu município de residência?',
        'município de residência',
        'cidade',
        'Cidade',
        'Município',
        'municipio'
    ]
    
    for col in possiveis_colunas:
        if col in df.columns:
            coluna_cidade = col
            break
    
    if not coluna_cidade:
        return jsonify(error="Coluna de cidade não encontrada no CSV"), 400
    
    # Conta alunos por cidade
    cidades_count = df[coluna_cidade].value_counts().to_dict()
    
    # Coordenadas aproximadas das principais cidades de SC
    coordenadas_cidades = {
        'Palhoça': {'lat': -27.6453, 'lng': -48.6697, 'nome': 'Palhoça'},
        'Florianópolis': {'lat': -27.5954, 'lng': -48.5480, 'nome': 'Florianópolis'},
        'São José': {'lat': -27.6146, 'lng': -48.6366, 'nome': 'São José'},
        'Biguaçu': {'lat': -27.4942, 'lng': -48.6556, 'nome': 'Biguaçu'},
        'Antônio Carlos': {'lat': -27.5194, 'lng': -48.7669, 'nome': 'Antônio Carlos'},
        'Santo Amaro da Imperatriz': {'lat': -27.6881, 'lng': -48.7786, 'nome': 'Santo Amaro da Imperatriz'},
        'Paulo Lopes': {'lat': -27.9617, 'lng': -48.6847, 'nome': 'Paulo Lopes'},
        'Garopaba': {'lat': -28.0239, 'lng': -48.6128, 'nome': 'Garopaba'},
        'Imbituba': {'lat': -28.2403, 'lng': -48.6703, 'nome': 'Imbituba'},
        'Tubarão': {'lat': -28.4800, 'lng': -49.0069, 'nome': 'Tubarão'},
        'Criciúma': {'lat': -28.6775, 'lng': -49.3697, 'nome': 'Criciúma'},
        'Blumenau': {'lat': -26.9194, 'lng': -49.0661, 'nome': 'Blumenau'},
        'Joinville': {'lat': -26.3044, 'lng': -48.8456, 'nome': 'Joinville'},
        'Chapecó': {'lat': -27.0969, 'lng': -52.6178, 'nome': 'Chapecó'},
    }
    
    # Processa dados
    dados_mapa = []
    total_alunos = 0
    cidades_encontradas = []
    
    for cidade, quantidade in cidades_count.items():
        cidade_limpa = str(cidade).strip()
        total_alunos += quantidade
        
        # Normaliza nome da cidade (remove acentos, maiúsculas)
        cidade_normalizada = cidade_limpa.lower()
        
        # Tenta encontrar coordenadas
        coords = None
        for nome_chave, dados in coordenadas_cidades.items():
            if nome_chave.lower() in cidade_normalizada or cidade_normalizada in nome_chave.lower():
                coords = dados
                coords['quantidade'] = int(quantidade)
                break
        
        # Se não encontrou, usa coordenadas padrão de Palhoça (centro da região)
        if not coords:
            coords = {
                'lat': -27.6453,
                'lng': -48.6697,
                'nome': cidade_limpa,
                'quantidade': int(quantidade)
            }
        else:
            coords['nome'] = cidade_limpa
        
        dados_mapa.append(coords)
        cidades_encontradas.append(cidade_limpa)
    
    # Encontra cidade com maior concentração
    cidade_maior = max(cidades_count.items(), key=lambda x: x[1]) if cidades_count else None
    
    return jsonify({
        'dados': dados_mapa,
        'estatisticas': {
            'total_alunos': total_alunos,
            'total_cidades': len(set(cidades_encontradas)),
            'maior_concentracao': cidade_maior[0] if cidade_maior else 'N/A',
            'alunos_maior_cidade': int(cidade_maior[1]) if cidade_maior else 0
        }
    })

# ---------------- API: VISUALIZAÇÕES COMPLETAS ----------------
@app.route('/api/visualizacoes_completas', methods=['POST'])
@login_required
def api_visualizacoes_completas():
    """Gera múltiplos gráficos dinâmicos, mapas de calor e mapas geográficos"""
    data = request.get_json()
    filename = data.get("filename")
    
    if not filename:
        return jsonify(error="Nenhum arquivo selecionado"), 400
    
    try:
        df = load_csv(filename)
    except Exception as e:
        return jsonify(error=f"Erro ao abrir arquivo: {e}"), 400
    
    resultados = []
    
    # Função auxiliar para converter figura Plotly para JSON
    def convert(fig_json):
        return json.loads(json.dumps(fig_json, default=str))
    
    # 1. GRÁFICO DE BARRAS - Distribuição por Curso
    try:
        coluna_curso = None
        for col in df.columns:
            if 'curso' in col.lower() or 'Curso' in col:
                coluna_curso = col
                break
        
        if coluna_curso:
            # Aplica abreviação de cursos
            df_curso = aplicar_abreviacao_cursos(df.copy(), coluna_curso)
            curso_counts = df_curso[coluna_curso].value_counts()
            fig_curso = px.bar(
                x=curso_counts.index,
                y=curso_counts.values,
                title="Distribuição de Alunos por Curso",
                labels={'x': 'Curso', 'y': 'Quantidade de Alunos'},
                color=curso_counts.values,
                color_continuous_scale='Blues'
            )
            fig_curso.update_layout(
                xaxis_tickangle=-45,
                height=400,
                showlegend=False
            )
            resultados.append({
                "tipo": "bar",
                "titulo": "Distribuição por Curso",
                "fig": convert(fig_curso.to_plotly_json())
            })
    except Exception as e:
        pass
    
    # 2. GRÁFICO DE PIZZA - Distribuição por Gênero
    try:
        coluna_genero = None
        for col in df.columns:
            if 'gênero' in col.lower() or 'genero' in col.lower() or 'identifica' in col.lower():
                coluna_genero = col
                break
        
        if coluna_genero:
            genero_counts = df[coluna_genero].value_counts()
            fig_genero = px.pie(
                values=genero_counts.values,
                names=genero_counts.index,
                title="Distribuição por Gênero",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_genero.update_layout(height=400)
            resultados.append({
                "tipo": "pie",
                "titulo": "Distribuição por Gênero",
                "fig": convert(fig_genero.to_plotly_json())
            })
    except Exception as e:
        pass
    
    # 3. GRÁFICO DE BARRAS - Faixa Etária
    try:
        coluna_idade = None
        for col in df.columns:
            if 'faixa etária' in col.lower() or 'idade' in col.lower():
                coluna_idade = col
                break
        
        if coluna_idade:
            idade_counts = df[coluna_idade].value_counts().sort_index()
            fig_idade = px.bar(
                x=idade_counts.index,
                y=idade_counts.values,
                title="Distribuição por Faixa Etária",
                labels={'x': 'Faixa Etária', 'y': 'Quantidade'},
                color=idade_counts.values,
                color_continuous_scale='Oranges'
            )
            fig_idade.update_layout(height=400, showlegend=False)
            resultados.append({
                "tipo": "bar",
                "titulo": "Distribuição por Faixa Etária",
                "fig": convert(fig_idade.to_plotly_json())
            })
    except Exception as e:
        pass
    
    # 4. HEATMAP - Curso vs Cidade
    try:
        if coluna_curso:
            coluna_cidade = None
            for col in df.columns:
                if 'município' in col.lower() or 'cidade' in col.lower() or 'residência' in col.lower():
                    coluna_cidade = col
                    break
            
            if coluna_cidade:
                # Aplica abreviação de cursos antes de criar o heatmap
                df_heatmap = aplicar_abreviacao_cursos(df.copy(), coluna_curso)
                pivot = pd.crosstab(df_heatmap[coluna_curso], df_heatmap[coluna_cidade], margins=False)
                fig_heatmap = px.imshow(
                    pivot.values,
                    labels=dict(x="Cidade", y="Curso", color="Quantidade"),
                    x=pivot.columns,
                    y=pivot.index,
                    title="Heatmap: Curso vs Cidade",
                    color_continuous_scale='YlOrRd',
                    aspect="auto"
                )
                fig_heatmap.update_layout(height=500)
                resultados.append({
                    "tipo": "heatmap",
                    "titulo": "Heatmap: Curso vs Cidade",
                    "fig": convert(fig_heatmap.to_plotly_json())
                })
    except Exception as e:
        pass
    
    # 5. GRÁFICO DE BARRAS HORIZONTAIS - Cor/Raça
    try:
        coluna_cor = None
        for col in df.columns:
            if 'cor' in col.lower() or 'raça' in col.lower():
                coluna_cor = col
                break
        
        if coluna_cor:
            cor_counts = df[coluna_cor].value_counts()
            fig_cor = px.bar(
                x=cor_counts.values,
                y=cor_counts.index,
                orientation='h',
                title="Distribuição por Cor/Raça",
                labels={'x': 'Quantidade', 'y': 'Cor/Raça'},
                color=cor_counts.values,
                color_continuous_scale='Viridis'
            )
            fig_cor.update_layout(height=400, showlegend=False)
            resultados.append({
                "tipo": "bar_h",
                "titulo": "Distribuição por Cor/Raça",
                "fig": convert(fig_cor.to_plotly_json())
            })
    except Exception as e:
        pass
    
    # 6. GRÁFICO DE BARRAS - Meio de Divulgação
    try:
        coluna_divulgacao = None
        for col in df.columns:
            if 'divulgação' in col.lower() or 'conheceu' in col.lower():
                coluna_divulgacao = col
                break
        
        if coluna_divulgacao:
            div_counts = df[coluna_divulgacao].value_counts()
            fig_div = px.bar(
                x=div_counts.index,
                y=div_counts.values,
                title="Como os Alunos Conheceram a FMP",
                labels={'x': 'Meio de Divulgação', 'y': 'Quantidade'},
                color=div_counts.values,
                color_continuous_scale='Purples'
            )
            fig_div.update_layout(xaxis_tickangle=-45, height=400, showlegend=False)
            resultados.append({
                "tipo": "bar",
                "titulo": "Meio de Divulgação",
                "fig": convert(fig_div.to_plotly_json())
            })
    except Exception as e:
        pass
    
    # 7. GRÁFICO DE BARRAS - Situação de Trabalho
    try:
        coluna_trabalho = None
        for col in df.columns:
            if 'trabalhando' in col.lower() or 'trabalha' in col.lower():
                coluna_trabalho = col
                break
        
        if coluna_trabalho:
            trab_counts = df[coluna_trabalho].value_counts()
            fig_trab = px.bar(
                x=trab_counts.index,
                y=trab_counts.values,
                title="Situação de Trabalho",
                labels={'x': 'Situação', 'y': 'Quantidade'},
                color=trab_counts.values,
                color_continuous_scale='Greens'
            )
            fig_trab.update_layout(height=400, showlegend=False)
            resultados.append({
                "tipo": "bar",
                "titulo": "Situação de Trabalho",
                "fig": convert(fig_trab.to_plotly_json())
            })
    except Exception as e:
        pass
    
    # 8. GRÁFICO DE BARRAS - Renda
    try:
        coluna_renda = None
        for col in df.columns:
            if 'renda' in col.lower():
                coluna_renda = col
                break
        
        if coluna_renda:
            renda_counts = df[coluna_renda].value_counts()
            # Ordena por ordem lógica de renda
            ordem_renda = [
                'Menos de 1 salário mínimo',
                'De 1 a 3 salários mínimos',
                'De 4 a 6 salários mínimos',
                'Mais de 6 salários mínimos'
            ]
            renda_ordenada = {}
            for ordem in ordem_renda:
                for key, value in renda_counts.items():
                    if ordem in str(key):
                        renda_ordenada[key] = value
                        break
            for key, value in renda_counts.items():
                if key not in renda_ordenada:
                    renda_ordenada[key] = value
            
            fig_renda = px.bar(
                x=list(renda_ordenada.keys()),
                y=list(renda_ordenada.values()),
                title="Distribuição por Faixa de Renda",
                labels={'x': 'Faixa de Renda', 'y': 'Quantidade'},
                color=list(renda_ordenada.values()),
                color_continuous_scale='Reds'
            )
            fig_renda.update_layout(xaxis_tickangle=-45, height=400, showlegend=False)
            resultados.append({
                "tipo": "bar",
                "titulo": "Distribuição por Renda",
                "fig": convert(fig_renda.to_plotly_json())
            })
    except Exception as e:
        pass
    
    # 9. HEATMAP DE CORRELAÇÃO (se houver colunas numéricas)
    try:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            fig_corr = px.imshow(
                corr_matrix.values,
                labels=dict(x="Variável", y="Variável", color="Correlação"),
                x=corr_matrix.columns,
                y=corr_matrix.index,
                title="Heatmap de Correlação entre Variáveis Numéricas",
                color_continuous_scale='RdBu',
                aspect="auto"
            )
            fig_corr.update_layout(height=500)
            resultados.append({
                "tipo": "heatmap",
                "titulo": "Correlação entre Variáveis",
                "fig": convert(fig_corr.to_plotly_json())
            })
    except Exception as e:
        pass
    
    # 10. DADOS PARA MAPA GEOGRÁFICO MELHORADO (com clusters)
    try:
        coluna_cidade = None
        for col in df.columns:
            if 'município' in col.lower() or 'cidade' in col.lower() or 'residência' in col.lower():
                coluna_cidade = col
                break
        
        if coluna_cidade:
            cidades_count = df[coluna_cidade].value_counts().to_dict()
            
            # Coordenadas das cidades
            coordenadas_cidades = {
                'Palhoça': {'lat': -27.6453, 'lng': -48.6697},
                'Florianópolis': {'lat': -27.5954, 'lng': -48.5480},
                'São José': {'lat': -27.6146, 'lng': -48.6366},
                'Biguaçu': {'lat': -27.4942, 'lng': -48.6556},
                'Antônio Carlos': {'lat': -27.5194, 'lng': -48.7669},
                'Santo Amaro da Imperatriz': {'lat': -27.6881, 'lng': -48.7786},
            }
            
            dados_mapa = []
            for cidade, quantidade in cidades_count.items():
                cidade_limpa = str(cidade).strip()
                coords = None
                for nome_chave, dados in coordenadas_cidades.items():
                    if nome_chave.lower() in cidade_limpa.lower() or cidade_limpa.lower() in nome_chave.lower():
                        coords = dados.copy()
                        coords['nome'] = cidade_limpa
                        coords['quantidade'] = int(quantidade)
                        break
                
                if not coords:
                    coords = {
                        'lat': -27.6453,
                        'lng': -48.6697,
                        'nome': cidade_limpa,
                        'quantidade': int(quantidade)
                    }
                
                dados_mapa.append(coords)
            
            resultados.append({
                "tipo": "mapa",
                "titulo": "Dados Geográficos para Mapa",
                "dados_mapa": dados_mapa,
                "estatisticas": {
                    'total_alunos': int(df[coluna_cidade].count()),
                    'total_cidades': len(set(df[coluna_cidade].dropna().astype(str))),
                    'maior_concentracao': max(cidades_count.items(), key=lambda x: x[1])[0] if cidades_count else 'N/A',
                    'alunos_maior_cidade': int(max(cidades_count.values())) if cidades_count else 0
                }
            })
    except Exception as e:
        pass
    
    return jsonify({"visualizacoes": resultados})

# ---------------- Rota para quem somos ----------------
@app.route('/quem_somos')
def quem_somos():
    return render_template('quem_somos.html')

# ---------------- Rodapé com verifiação de login ----------------
@app.context_processor
def inject_globals():
    return {
        'current_year': datetime.now().year,
        'is_logged': current_user.is_authenticated
    }


# ---------------- criar banco e rodar ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
