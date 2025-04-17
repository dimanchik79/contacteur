from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import current_user, login_required
from utils.lang import lang as LANG
from utils.utils import get_documents_level_zero, get_uniq, get_documents_by_uniq
from db.models import DB, Catalog

contacteur = Blueprint('contacteur', __name__)

IMG = ['img/folder.png', 'img/contact.png', 'img/note.png']

@contacteur.route('/', methods=['GET', 'POST'])
@login_required
def index() -> redirect:
    """Главная страница"""
    lng = current_user.language
    session['lng'] = lng
    return redirect(url_for('contacteur.navigation', level=0, uniq="None"))
    
    
@contacteur.route('/navigation/<int:level>/<uniq>', methods=['GET', 'POST'])
@login_required 
def navigation(level: int, uniq: str) -> render_template:
    """Навигация по дукументам"""
    error = ""
    _lng = session['lng']
    
    if level == 0:
        documents = get_documents_level_zero()
    else:
        documents = get_documents_by_uniq(uniq)
    print(documents)    
    if request.method == 'POST':
        if 'folder_add' in request.form:
            if request.form['folder_name'] == "":
                error = LANG['folder_name_error'][_lng]
            if not error:
                folder = Catalog(date=request.form['date'], 
                                uniq=get_uniq(),
                                type=0,
                                name=request.form['folder_name'], 
                                user_id=current_user.id,
                                level_0=True if level == 0 else False)
                DB.session.add(folder)
                DB.session.commit()
                return redirect(url_for('contacteur.navigation', level=level, uniq=uniq))
    return render_template('contacteur/index.html',
                           error=error,
                           title=LANG['contacteur_title'][_lng],
                           language=LANG,
                           _lng=_lng,
                           level=level,
                           documents=documents,
                           img=IMG)
    


# ABOUT PAGE
# @homeblock.route('/about', methods=['GET', 'POST'])
# @login_required
# def about() -> render_template:
#     """О нас"""
#     return render_template('about.html', user=current_user, catalog=get_catalog(0))