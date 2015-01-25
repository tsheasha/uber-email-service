from flask import Blueprint, render_template

# Creating an Index Blueprint in an effort to make the applicaiton Modular
index_blueprint = Blueprint('index', __name__)

# Render index.html template
@index_blueprint.route('/')
def index():
    return render_template('index.html')
