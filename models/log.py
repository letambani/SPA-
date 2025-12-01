from datetime import datetime
from models.user import db

class Log(db.Model):
    __tablename__ = 'log'

    id_log = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    acao = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    ip = db.Column(db.String(45))
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Log {self.acao} - Usuário {self.id_usuario}>"
