from app import db
from app.search import add_to_index, remove_from_index, query_index, query_index_content
#from app import app,db


# for debugging
import inspect

# ad hoc
#from flask import current_app

ROLE_USER = 0
ROLE_ADMIN = 1

class SearchableMixin(object):
	@classmethod
	def searchraw(cls, expression, page, per_page):
		ids, total = query_index(cls.__tablename__, expression, page, per_page)
		if total == 0:
			return cls.query.filter_by(id=0), 0
		when = []
		for i in range(len(ids)):
			when.append((ids[i], i))
		TextPairs = cls.query.filter(cls.id.in_(ids)).all()
		# print("DB array")
		# print("TextPairs typ: ", type(TextPairs))
		# print("TextPairs len: ", len(TextPairs))
		paracount = 0
		parags = []
		for pair in TextPairs:
			phraseorig = pair.vntext
			phrasetran = pair.rutext
			print('phraseorig :', phraseorig)
			
			paracount += 1
			parag = {
				'count': str(paracount),
				'origparts': parsestringtonicearray(phraseorig),
				'tranparts': parsestringtonicearray(phrasetran)
			}
			parags.append(parag)
			# print("Appended parag: ", parag)
		return parags, total
	
	@classmethod
	def search(cls, expression, page, per_page):
		ids, total = query_index(cls.__tablename__, expression, page, per_page)
		if total == 0:
			return cls.query.filter_by(id=0), 0
		when = []
		for i in range(len(ids)):
			when.append((ids[i], i))
		return cls.query.filter(cls.id.in_(ids)).order_by(
			db.case(when, value=cls.id)), total
	
	@classmethod
	def before_commit(cls, session):
		session._changes = {
			'add': list(session.new),
			'update': list(session.dirty),
			'delete': list(session.deleted)
		}
	
	@classmethod
	def after_commit(cls, session):
		for obj in session._changes['add']:
			if isinstance(obj, SearchableMixin):
				add_to_index(obj.__tablename__, obj)
		for obj in session._changes['update']:
			if isinstance(obj, SearchableMixin):
				add_to_index(obj.__tablename__, obj)
		for obj in session._changes['delete']:
			if isinstance(obj, SearchableMixin):
				remove_from_index(obj.__tablename__, obj)
		session._changes = None
	
	@classmethod
	def reindex(cls):
		for obj in cls.query:
			add_to_index(cls.__tablename__, obj)
	
#db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
#db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

class TextPair(SearchableMixin, db.Model):
	__searchable__ = ['rutext','vntext']
	id = db.Column(db.Integer, primary_key = True)
	vntext = db.Column(db.String(400))
	rutext = db.Column(db.String(400))
	comment = db.Column(db.String(400))
	#datestring = db.Column(db.String(40))
	
	def __repr__(self):
		return '<Pair %r>' % (self.vntext)
	
	@classmethod
	def search(cls, expression, page, per_page):
		if not app.elasticsearch:
			return [], 0
		ids, total = query_index_content(cls.__tablename__, expression, page, per_page)
		if total == 0:
			return cls.query.filter_by(id=0), 0
		return ids, total
		when = []	
		for i in range(len(ids)):
			when.append((ids[i], i))
			print(ids[i])	
		return when

from app.views import parsestringtonicearray