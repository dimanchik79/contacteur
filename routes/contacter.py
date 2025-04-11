from flask import Blueprint, render_template
from flask_login import current_user, login_required
from utils.lang import lang as LANG

contacteur = Blueprint('contacteur', __name__)

@contacteur.route('/', methods=['GET', 'POST'])
@login_required
def index() -> render_template:
    """Главная страница"""
    return render_template('contacteur/index.html', language=LANG)


# ABOUT PAGE
# @homeblock.route('/about', methods=['GET', 'POST'])
# @login_required
# def about() -> render_template:
#     """О нас"""
#     return render_template('about.html', user=current_user, catalog=get_catalog(0))