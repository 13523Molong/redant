
from flask import Blueprint

bp = Blueprint('utils', __name__)

@bp.route('/')
def index():
    return 'Index Page'
