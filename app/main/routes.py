#from flask import g
# from git
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app

# ad hoc
from app import db
from app.models import TextPair

from app.main.forms import SearchForm

# ad hoc
from flask import request

#bp kostyl
from app.main import bp

@bp.before_app_request
def before_request():
	#if current_user.is_authenticated:
	#current_user.last_seen = datetime.utcnow()
	#b.session.commit()
	g.search_form = SearchForm()
    #g.locale = str(get_locale())

@bp.route('/search')
#@login_required
def search():
	if not g.search_form.validate():
		return redirect(url_for('main.explore'))
	page = request.args.get('page', 1, type=int)
	parags, total = TextPair.search(g.search_form.q.data, page, 10)
	#						   current_app.config['POSTS_PER_PAGE'])							   
	return render_template('search.html', title=_('Search'), parags=parags)