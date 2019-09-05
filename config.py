import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
	#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	# default True is deprecated
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	#ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
	ELASTICSEARCH_URL = 'http://localhost:9200'

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
##app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
## default True is deprecated
#SQLALCHEMY_TRACK_MODIFICATIONS = False