import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# default True is deprecated
SQLALCHEMY_TRACK_MODIFICATIONS = False
