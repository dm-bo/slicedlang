from flask import Blueprint

# bp kostyl
from app import app

bp = Blueprint('main', __name__)

from app.main import routes
