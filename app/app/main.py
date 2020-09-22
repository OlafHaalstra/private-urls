# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db, create_app

from .models import Link, View

main = Blueprint('main', __name__)

@main.route('/admin')
def index():
    return render_template('admin.html')

@main.route('/profile')
@login_required
def profile():
    links = Link.query.all()
    return render_template('profile.html', name=current_user.name, links=links)

if __name__ == "__main__":
    app = create_app()
    db.create_all(app=app)
    app.run()
else:
    application = create_app()
