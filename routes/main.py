from flask import Blueprint, render_template, request, jsonify
main_routes = Blueprint('main_routes', __name__, url_prefix='/')

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/info')
def test():
    return render_template('info.html')
@main_routes.route('/control')
def control():
    return render_template('control.html')