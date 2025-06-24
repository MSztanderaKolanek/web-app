class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass@localhost:5432/webappdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'pass'
