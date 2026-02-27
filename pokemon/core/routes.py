from flask import Blueprint, render_template, request, abort
from pokemon.extension import db
from pokemon.models import Pokemon, Type


core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
    page = request.args.get('page',type=int)
    pokemons = db.paginate(db.select(Pokemon), per_page=4, page=page)
    return render_template('core/index.html', title='Home Page', page=page, pokemons=pokemons )

@core_bp.route('/<int:id>/details')
def details(id):
    pokemon = db.session.get(Pokemon, id)
    if not pokemon:
        abort(404)
    return render_template('core/pokemon_detail.html', title='Details Page', pokemon=pokemon)

