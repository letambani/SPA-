import os

class Config:
    SECRET_KEY = 'sua_chave_secreta_aqui'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/spa?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuração de e-mail (SSL)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'marcelo.marq2001@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')  # Aqui precisa pegar a senha de app do email que faz o envio de recuperação
    MAIL_DEFAULT_SENDER = ('FMPSC - SPA', os.getenv('MAIL_USERNAME', 'marcelo.marq2001@gmail.com'))
