from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

#class TextPair(db.Model):
class TextPair(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	vntext = db.Column(db.String(400))
	rutext = db.Column(db.String(400))
	comment = db.Column(db.String(400))
	#datestring = db.Column(db.String(40))
	
	def __repr__(self):
		return '<Pair %r>' % (self.vntext)