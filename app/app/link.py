
import secrets
from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory, Response
from flask_login import login_required, current_user
from .models import Link, View
from . import db
import requests
from urllib.parse import urlparse

link = Blueprint('link', __name__)

@link.route('/create', methods=['POST'])
@login_required
def create_post():
    new_link = Link(suffix=secrets.token_urlsafe(6), description=request.form.get('description'))

    # add the new link suffix to the database
    db.session.add(new_link)
    db.session.commit()

    return redirect(url_for('main.profile'))

@link.route('/',methods=["GET"], defaults={'path': 'index.html'})
@link.route('/<path:path>',methods=["GET"])
def proxy(path):
    # Check database
    referrer = request.referrer
    
    # print(referrer.args.get('k'))
    suffix = request.args.get('k')
    if not suffix:
        query = urlparse(referrer).query
        if query: 
            suffix = query.split('=')[1]
    link = Link.query.filter_by(suffix=suffix).first()
    if not link:
        # return redirect(url_for('main.index'))
        SITE_NAME = 'http://public:4000'
    else:
        SITE_NAME = 'http://private:5000'
        new_view = View(link=link)

        db.session.add(new_view)
        db.session.commit()
    
    # Return site on other server
    resp = requests.get(f'{SITE_NAME}/{path}')
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)
    return response