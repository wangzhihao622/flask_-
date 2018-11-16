import os
class Config():
    DEBUG = True

    SECRET_KEY = os.urandom(24)
    #
    # HOSTNAME   = 'localhost'
    # PORT       = '3306'
    # DATABASE   = 'flask_blog'
    # USERNAME    = 'root'
    # PASSWORD   = '123456'
    # DB_URI ='mysql+pymysql://{}:{}@{}:{}/{}?charset=utf-8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:123456@localhost:3306/flask_blog'

    SQLALCHEMY_TRACK_MODIFICATIONS = False