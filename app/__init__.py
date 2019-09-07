from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy
from config import Config
from flask_sqlalchemy import SQLAlchemy
# obsolete
###from flask_migrate import Migrate

from elasticsearch import Elasticsearch

app = Flask(__name__)
app.config.from_object(Config)

from app.main import bp as main_bp
app.register_blueprint(main_bp)

#db = SQLAlchemy(app)
#git
db = SQLAlchemy()

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
	if app.config['ELASTICSEARCH_URL'] else None

# obsolete
####migrate = Migrate(app, db)

from app import views, models