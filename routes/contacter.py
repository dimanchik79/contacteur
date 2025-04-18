from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import current_user, login_required
from utils.lang import lang as LANG
from utils.utils import add_document, get_documents_level_zero, get_documents_by_uniq
from db.models import DB

contacteur = Blueprint('contacteur', __name__)
FOLDERS_PATH = []

IMG = ['img/folder.png', 'img/contact.png', 'img/note.png']

@contacteur.route('/', methods=['GET', 'POST'])
@login_required
def index() -> redirect:
    """Главная страница"""
    lng = current_user.language
    session['lng'] = lng
    FOLDERS_PATH.clear()
    return redirect(url_for('contacteur.navigation', level=0, parent="None", name="None"))
    
    
@contacteur.route('/navigation/<int:level>/<parent>/<name>', methods=['GET', 'POST'])
@login_required 
def navigation(level: int, parent: str, name: str) -> render_template:
    """Навигация по дукументам"""
    error = ""
    _lng = session['lng']
    
    if level == 0:
        documents = get_documents_level_zero()
    else:
        documents = get_documents_by_uniq(parent, name)
        FOLDERS_PATH.append({'parent': parent, 'name': name, 'level': level, 'type': 0})

    if request.method == 'POST':
        if 'folder_add' in request.form:
            if request.form['folder_name'] == "":
                error = LANG['folder_name_error'][_lng]
            if not error:
                add_document(request, level, parent, type_doc=0)
                return redirect(url_for('contacteur.navigation', level=level, parent=parent, name=name))
            
    return render_template('contacteur/index.html',
                           error=error,
                           title=LANG['contacteur_title'][_lng],
                           language=LANG,
                           _lng=_lng,
                           level=level,
                           name=name,
                           parent=parent,
                           documents=documents,
                           img=IMG)
    
@contacteur.route('/back/<int:level>/<parent>/<name>', methods=['GET', 'POST'])
@login_required
def back(level: int, parent: str, name: str) -> redirect:
    """Навигация назад по дукументам"""
    level -= 1
    if level == 0:
        return redirect(url_for('.index'))
    FOLDERS_PATH.pop()
    return redirect(url_for('contacteur.navigation', level=FOLDERS_PATH[-1]['level'], parent=FOLDERS_PATH[-1]['parent'], name=FOLDERS_PATH[-1]['name']))    

# ABOUT PAGE
# @homeblock.route('/about', methods=['GET', 'POST'])
# @login_required
# def about() -> render_template:
#     """О нас"""
#     return render_template('about.html', user=current_user, catalog=get_catalog(0))