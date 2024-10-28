import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:prastita15@localhost:5432/prak6sig')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    