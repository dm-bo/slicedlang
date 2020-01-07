from flask import g
# from git
from flask import render_template
# strange import
# from flask import render_template, flash, redirect, url_for, request, g, \
#    jsonify, current_app

# ad hoc
# from app import db
from models import TextPair

from main.forms import SearchForm

# ad hoc
from flask import request

from main import bp

@bp.before_app_request
def before_request():
    # if current_user.is_authenticated:
    # current_user.last_seen = datetime.utcnow()
    # b.session.commit()
    g.search_form = SearchForm()


# g.locale = str(get_locale())

@bp.route('/', strict_slashes=False)
@bp.route('/search')
# @login_required
def search():
    if not g.search_form.validate():
        # return redirect(url_for('main.explore'))
        return render_template('search.html', title='Search', parags=[])
    # какая страница нужна? (из args) По дефолту первая
    page = request.args.get('page', 1, type=int)
    parags, total = TextPair.searchraw(g.search_form.q.data, page, 10)
    #						   current_app.config['POSTS_PER_PAGE'])
    # FIXME useless "title"
    if total == 0:
        return render_template('search.html', title='Search', parags=[], total=total, query=g.search_form.q.data)
    else:
        return render_template('search.html', title='Search', parags=parags, total=total, query=g.search_form.q.data)

@bp.route('/about')
def showabout():
    return render_template("about.html")

