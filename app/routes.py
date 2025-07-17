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

@url_routes.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        url.clicks += 1
        db.session.commit()
        return redirect(url.original_url)
    return jsonify({'error': 'Short URL not found'}), 404


@url_routes.route('/stats/<short_code>', methods=['GET'])
def get_url_stats(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        return jsonify({
            'original_url': url.original_url,
            'short_code': url.short_code,
            'clicks': url.clicks,
            'created_at': url.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({'error': 'Short URL not found'}), 404
