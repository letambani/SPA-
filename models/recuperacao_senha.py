from datetime import datetime, timedelta
from models.user import db
import secrets

class RecuperacaoSenha(db.Model):
    __tablename__ = 'recuperacao_senha'

    id_recuperacao = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_expiracao = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def gerar_token(id_usuario):
        token = secrets.token_urlsafe(32)
        expira = datetime.utcnow() + timedelta(hours=1)
        rec = RecuperacaoSenha(id_usuario=id_usuario, token=token, data_expiracao=expira)
        db.session.add(rec)
        db.session.commit()
        return token
