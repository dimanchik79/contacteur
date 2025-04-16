from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import current_user, login_required
from utils.lang import lang as LANG

contacteur = Blueprint('contacteur', __name__)

@contacteur.route('/', methods=['GET', 'POST'])
@login_required
def index() -> redirect:
    """Главная страница"""
    lng = current_user.language
    session['lng'] = lng
    return redirect(url_for('contacteur.navigation', level=0))
    
    
@contacteur.route('/navigation/<int:level>', methods=['GET', 'POST'])
@login_required 
def navigation(level):
    _lng = session['lng']
    return render_template('contacteur/index.html', 
                           title=LANG['contacteur_title'][_lng],
                           language=LANG,
                           _lng=_lng,
                           level=level)
    


# ABOUT PAGE
# @homeblock.route('/about', methods=['GET', 'POST'])
# @login_required
# def about() -> render_template:
#     """О нас"""
#     return render_template('about.html', user=current_user, catalog=get_catalog(0))