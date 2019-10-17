from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy
from config import Config
from flask_sqlalchemy import SQLAlchemy
# obsolete
###from flask_migrate import Migrate

from elasticsearch import Elasticsearch

#db = SQLAlchemy(app)
#git

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from main import bp as main_bp
app.register_blueprint(main_bp)

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
	if app.config['ELASTICSEARCH_URL'] else None

