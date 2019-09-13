import os

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')

print(db_user)
print(db_password)

class Config():
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://fikriamri:threecheers@127.0.0.1:3306/e_commerce_project'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:Altabatch3@e-commerce-project.cvz8vemwkkzi.ap-southeast-1.rds.amazonaws.com:3306/e_commerce_project'

class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://fikriamri:threecheers@127.0.0.1:3306/e_commerce_project_testing'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:Altabatch3@e-commerce-project.cvz8vemwkkzi.ap-southeast-1.rds.amazonaws.com:3306/e_commerce_project_testing'