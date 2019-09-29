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
# not installed in new version, skipping
from elasticsearch import Elasticsearch
from flask import Flask, jsonify #, request

# obsolete
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





