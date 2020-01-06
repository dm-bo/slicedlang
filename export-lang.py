from elasticsearch import Elasticsearch
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import re

import argparse
parser = argparse.ArgumentParser(description='Exporting CSV files.')
parser.add_argument('infile', type=str, help='Input file')
args = parser.parse_args()

#### SQL ####
# https://ru.wikibooks.org/wiki/SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app/app.db')
Session = sessionmaker()
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
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
	#TextPair.__table__.drop(engine)
	print("No DB drop.")
except:
	print("No base, no care.")

Base.metadata.create_all(engine)

#### ES ####
es = Elasticsearch('http://localhost:9200')
#datapath = 'data/text_pair.csv'
datapath = args.infile
try:
	print('Left ES undeleted...')
	#es.indices.delete('text_pair')
except:
	print("C'est la vie")

#### Action for both ####

num_lines = sum(1 for line in open(datapath, 'r', encoding='utf8'))
print("Working on",num_lines,"lines...")

f = open(datapath, 'r', encoding='utf8')

id = 0
counter = 0
session = Session()
for line in f:
	counter = counter + 1
	line_arr = line.split(";")
	
	# check if line is empty
	emptypattern = re.compile("^$")
	if emptypattern.match(line):
		print("No data at line #",counter)
		continue
	
	# check if line is comment
	commentpattern = re.compile("^#")
	if commentpattern.match(line):
		print("Skippng comment at line #",counter)
		continue
	
	# check if line consist of 4 parts
	if len(line_arr) != 4:
		print("Not ok parts",len(line_arr),"at line",counter)
		continue
	
	# Get data: id and pair of tagged texts
	id = line_arr[0]
	tagvntext = line.split(";")[1]
	tagrutext = line.split(";")[2]
	
	# Check if record should be removed instead of upserted
	if tagvntext == "(deleted)" or tagrutext == "(deleted)":
		print("Removing textpair at line", counter, "( id =", id, ")")
		try:
			es.delete(index="text_pair",doc_type="text_pair",id=id)
		except:
			print("id", id,"not found, possibly already removed.")
		# not sure if it works
		session.query(TextPair).filter(TextPair.id==id).delete()
		continue

	# Remove tags and get untagged text for full-text search (this goes to Elastic)
	vntext = re.sub(r'#\d+', '', tagvntext)
	rutext = re.sub(r'#\d+', '', tagrutext)
	#print("2ES: ", id, " ", vntext, " ", rutext)
	es.index(index='text_pair', doc_type='text_pair', id=id, body={'vntext': vntext, 'rutext': rutext})
	
	#print("2SQL: ", id, " ", tagvntext, " ", tagrutext)
	tp = TextPair(id=id,vntext=tagvntext, rutext=tagrutext)
	session.query(TextPair).filter(TextPair.id==id).delete()
	session.commit()
	session.add(tp)
	session.commit()
	print(counter, end = "\r")
print("Completed.")
exit()
