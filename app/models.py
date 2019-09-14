from app import app,db
from app.search import add_to_index, remove_from_index, query_index, query_index_content

# for debugging
import inspect

ROLE_USER = 0
ROLE_ADMIN = 1

from app.search import add_to_index, remove_from_index, query_index

class SearchableMixin(object):
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
	
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

#class TextPair(db.Model):
class TextPair(db.Model):
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
		#return cls.query.filter(cls.id.in_(ids)).order_by(
		#	db.case(when, value=cls.id)), total
	
	@classmethod
	def searchraw(cls, expression, page, per_page):
		if not app.elasticsearch:
			return [], 0
		#print(inspect.getmembers(app.elasticsearch.search))
		search = app.elasticsearch.search(
			#index='my_textpairs', doc_type='textpairs',
			index='my_textpairs',
			body={'query': {'multi_match': {'query': expression, 'fields': ['*']}},
				  'from': (page - 1) * per_page, 'size': per_page})
		# search = app.elasticsearch.search(
			# index=index, doc_type=index,
			# body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
				  # 'from': (page - 1) * per_page, 'size': per_page})
		ids = [int(hit['_id']) for hit in search['hits']['hits']]
		return ids, search['hits']['total']
		return [], 0