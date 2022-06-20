from flask import Blueprint

blueprint = Blueprint('blueprint', __name__, static_folder='static', template_folder='templates')
