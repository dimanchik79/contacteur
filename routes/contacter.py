from flask import Blueprint, render_template, session
from flask_login import current_user, login_required
from utils.lang import lang as LANG

contacteur = Blueprint('contacteur', __name__)

@contacteur.route('/<int:level>', methods=['GET', 'POST'])
@login_required
def index(level) -> render_template:
    """Главная страница"""
    lng = current_user.language
    session['lng'] = lng
    return render_template('contacteur/index.html', 
                           title=LANG['contacteur_title'][lng],
                           language=LANG,
                           _lng=lng,
                           level=level)


# ABOUT PAGE
# @homeblock.route('/about', methods=['GET', 'POST'])
# @login_required
# def about() -> render_template:
#     """О нас"""
#     return render_template('about.html', user=current_user, catalog=get_catalog(0))