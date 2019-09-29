from flask import current_app

# for parsing (not good)
import re

def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, doc_type=index, id=model.id,
                                    body=payload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)

def query_index(index, query, page, per_page):
	if not current_app.elasticsearch:
		return [], 0
	print(index)
	search = current_app.elasticsearch.search(
		index=index,
		#index=index, doc_type=index,
		#index='my_textpairs', doc_type='textpairs',
		body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
			  'from': (page - 1) * per_page, 'size': per_page})
	# search = app.elasticsearch.search(
		# index=index, doc_type=index,
		# body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
			  # 'from': (page - 1) * per_page, 'size': per_page})
	ids = [int(hit['_id']) for hit in search['hits']['hits']]
	print('Returning:')
	print(ids)
	return ids, search['hits']['total']

def query_index_content(index, query, page, per_page):
	if not current_app.elasticsearch:
		return [], 0
	print(index)
	search = current_app.elasticsearch.search(
		index=index,
		#index=index, doc_type=index,
		#index='my_textpairs', doc_type='textpairs',
		body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
			  'from': (page - 1) * per_page, 'size': per_page})
	# search = app.elasticsearch.search(
		# index=index, doc_type=index,
		# body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
			  # 'from': (page - 1) * per_page, 'size': per_page})
	#ids = [int(hit['_id']) for hit in search['hits']['hits']]
	parags = []
	print('Forming parags...')
	if search['hits']['total'] == 0:
		print('We havent(')
		return [], 0
	for hit in search['hits']['hits']:
		parag = {
			'count': str(hit['_id']),
			'origparts': parsestringtonicearray(hit['_source']['rutext']),
			'tranparts': parsestringtonicearray(hit['_source']['vntext'])
		}
		print(hit['_id'])
		print(hit['_source']['vntext'])
		parags.append(parag)
	#print('Returning:')
	#print(parags)
	return parags, search['hits']['total']

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
