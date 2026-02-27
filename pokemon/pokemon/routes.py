from flask import Blueprint, render_template, redirect, url_for, flash, request
from pokemon.extension import db
from pokemon.models import Pokemon, User,Type
from flask_login import current_user, login_required


pokemon_bp = Blueprint('pokemon', __name__, template_folder='templates')

@pokemon_bp.route('/')
def index():
    query = db.select(Pokemon).where(Pokemon.user == current_user)
    pokemons = db.session.scalars(query).all()
    return render_template('pokemon/index.html', title='Pokemon Page', pokemons=pokemons)

@pokemon_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_pokemon():
    pokemon_types = db.session.scalars(db.select(Type)).all()
    if request.method == 'POST':
        name = request.form.get('name')
        height = request.form.get('height')
        weight = request.form.get('weight')
        description = request.form.get('description')
        img_url = request.form.get('img_url')
        type_id = request.form.getlist('pokemon_types')
        user_id = current_user.id

        p_type = []
        for id in type_id:
            p_type.append(db.session.get(Type, id))

        pokemon = Pokemon(
            name=name,
            height=height,
            weight=weight,
            description=description,
            img_url=img_url,
            user_id=user_id,
            types=p_type
        )
        db.session.add(pokemon)
        db.session.commit()
        flash(f'New Pokemon {name} has been added', 'success')
        return redirect(url_for('pokemon.index'))
    
    return render_template('pokemon/new_pokemon.html', title='New Pokemon Page', pokemon_types=pokemon_types)

