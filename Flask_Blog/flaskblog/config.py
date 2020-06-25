import os
class Config:
    SECRET_KEY              = '48b95e763384fd9a92ff9bd0111f0b18'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER             = 'smtp.googlemail.com'
    MAIL_PORT               = 587
    MAIL_USE_TLS            = True
    MAIL_USERNAME           = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD           = os.environ.get('EMAIL_PASS')

