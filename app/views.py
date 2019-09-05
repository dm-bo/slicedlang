from flask import render_template
from app import app #, db
# true need for generator
import re
# temporary need
import fileinput
from flask import request
# DB
from app.models import TextPair
# experimental
from elasticsearch import Elasticsearch

@app.route('/editor', methods=['GET', 'POST'])
def editor():
	textL1 = "cat eats notepad";
	textL2 = "кот жре матчасть";
	app.logger.info(request.args)
	app.logger.info(request.args.get(id))
	#try:
	#	app.logger.info(request.args.get(id))
	#except:
	#	whatweedit = "new record"
	#else:
	#	whatweedit = request.args.get(id)
	whatweedit = request.args.get(id)
	return render_template("edit2.html",
		textL1 = textL1,
		textL2 = textL2,
		whatweedit = whatweedit)

@app.route('/lingua')
def dualvocalbuary():
	TextPairs = TextPair.query
	paracount = 0
	parags = []
	for pair in TextPairs:
		phraseorig = pair.vntext
		phrasetran = pair.rutext
		
		paracount += 1
		parag = {
			'count': str(paracount),
			'origparts': parsestringtonicearray(phraseorig),
			'tranparts': parsestringtonicearray(phrasetran)
		}
		parags.append(parag)
	return render_template("bilingua.html",
		parags = parags)

def parsestringtonicearray(opstring):
	opwords = opstring.split("#")
	nicearray = []
	for opword in opwords:
		#app.logger.info("opword:: " + opword)
		tagnumber = re.search(r"^\d+",opword)
		if tagnumber:
			tnum = tagnumber.group(0)
			nextpart = {
				'tagnumber': tnum,
				'part': opword.replace(tnum, '', 1)
			}
			#app.logger.info("appending:: " + opword.replace(tnum, '', 1))
		else:
			nextpart = {
				'part': opword
			}
			#app.logger.info("appending:: " + opword)
		nicearray.append(nextpart)
	return nicearray

@app.route('/elastic')
def elasticview():
	es = Elasticsearch('http://localhost:9200')
	print("We are alive")
	return "hehe"

def query_index(index, query, page, per_page):
	if not es:
		return [], 0
	search = es.search(
		index=index, doc_type=index,
		body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
		      'from': (page - 1) * per_page, 'size': per_page})
	ids = [int(hit['_id']) for hit in search['hits']['hits']]
	return ids, search['hits']['total']




