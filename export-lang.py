from elasticsearch import Elasticsearch
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

#### SQL ####
# https://ru.wikibooks.org/wiki/SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
Session = sessionmaker()
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session.configure(bind=engine)

Base = declarative_base()
class TextPair(Base):
	__tablename__ = 'text_pair'
	id = Column(Integer, primary_key = True)
	vntext = Column(String(400))
	rutext = Column(String(400))
	comment = Column(String(400))
	
	def __init__(self, id, vntext, rutext):
		self.id = id
		self.vntext = vntext
		self.rutext = rutext
		#comment = db.Column(db.String(400))
	def __repr__(self):
		return "<User('%s','%s', '%s')>" % (self.id, self.vntext, self.rutext)

try:
	# https://stackoverflow.com/questions/35918605/how-to-delete-a-table-in-sqlalchemy
	TextPair.__table__.drop(engine)
except:
	print("No base, no care.")

Base.metadata.create_all(engine)

#### ES ####

es = Elasticsearch('http://localhost:9200')
f = open('data\\text_pair.csv', 'r', encoding='utf8')

try:
	print('no del')
	#es.indices.delete('text_pair')
except:
	print("C'est la vie")

#### Action for both ####

id = 0
for line in f:
	id = line.split(";")[0]
	#print(line)
	vntext = line.split(";")[3]
	#print(vntext)
	rutext = line.split(";")[4]
	print("2ES: ", id, " ", vntext, " ", rutext)
	es.index(index='text_pair', doc_type='text_pair', id=id, body={'vntext': vntext, 'rutext': rutext})
	
	#print(line)
	tagvntext= line.split(";")[1]
	#print(vntext)
	tagrutext = line.split(";")[2]
	print("2SQL: ", id, " ", tagvntext, " ", tagrutext)
	tp = TextPair(id=id,vntext=tagvntext, rutext=tagrutext)
	session = Session()
	session.add(tp)
	session.commit()
exit()