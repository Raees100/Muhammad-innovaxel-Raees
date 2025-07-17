from flask import Blueprint, request, jsonify, redirect
from .models import db, URL
import string, random

url_routes = Blueprint('url_routes', __name__)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

@url_routes.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('original_url')

    if not original_url:
        return jsonify({'error': 'Original URL is required'}), 400

    short_code = generate_short_code()
    while URL.query.filter_by(short_code=short_code).first():
        short_code = generate_short_code()

    new_url = URL(original_url=original_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        'original_url': original_url,
        'short_code': short_code
    }), 201
