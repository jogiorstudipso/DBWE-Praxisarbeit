import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# Lädt Umgebungsvariablen lokal aus .env (falls vorhanden).
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SERVER_NAME = os.environ.get('SERVER_NAME')

    db_url = os.environ.get('DATABASE_URL', '').strip()
    # Kompatibilität zu alten Postgres-URL-Schemata.
    db_url = db_url.replace('postgres://', 'postgresql://')
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set (MySQL is required for this project).")
    # Fallback auf PyMySQL-Treiber, falls nur mysql:// gesetzt wurde.
    if db_url.startswith('mysql://'):
        db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
    SQLALCHEMY_DATABASE_URI = db_url
    
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    REDIS_URL = os.environ.get('REDIS_URL') # optional
    POSTS_PER_PAGE = 25
