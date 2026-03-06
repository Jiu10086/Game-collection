from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app.extension import db
from app.models import Game
from flask_login import current_user, login_required

PLATFORMS = ['PC', 'PS5', 'PS4', 'Xbox', 'Nintendo Switch', 'Mobile']
GENRES = ['RPG', 'Action', 'FPS', 'Puzzle', 'Adventure', 'Strategy', 'Sports', 'Indie', 'Soul-like', 'Horror', 
          'Simulation', 'MMO', 'Fighting', 'Racing', 'Platformer', ''
          'Sandbox', 'Survival', 'Visual Novel', 'Stealth', 'Rhythm']
STATUSES = ['playing', 'completed', 'want_to_play', 'dropped']

games_bp = Blueprint('games', __name__, template_folder='templates')

@games_bp.route('/')
@login_required
def index():
    query = db.select(Game).where(Game.user_id == current_user.id)
    games = db.session.scalars(query).all()
    return render_template('games/index.html', title='My Games', games=games)

@games_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_game():
    if request.method == 'POST':
        title = request.form.get('title')
        platform = ', '.join(request.form.getlist('platform'))
        genre = ', '.join(request.form.getlist('genre'))
        status = request.form.get('status')
        rating = request.form.get('rating', type=int)
        image_url = request.form.get('image_url')
        note = request.form.get('note')

        game = Game(
            title=title,
            platform=platform,
            genre=genre,
            status=status,
            rating=rating,
            image_url=image_url,
            note=note,
            user_id=current_user.id
        )
        db.session.add(game)
        db.session.commit()
        flash(f'Game "{title}" has been added!', 'success')
        return redirect(url_for('games.index'))

    return render_template('games/new_game.html', title='Add Game',
                           platforms=PLATFORMS, genres=GENRES, statuses=STATUSES)

@games_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_game(id):
    game = db.session.get(Game, id)
    if not game or game.user_id != current_user.id:
        flash('Game not found.', 'danger')
        return redirect(url_for('games.index'))

    if request.method == 'POST':
        game.title = request.form.get('title')
        game.platform = ', '.join(request.form.getlist('platform'))
        game.genre = ', '.join(request.form.getlist('genre'))
        game.status = request.form.get('status')
        game.rating = request.form.get('rating', type=int)
        game.image_url = request.form.get('image_url')
        game.note = request.form.get('note')

        db.session.commit()
        flash(f'Game "{game.title}" has been updated!', 'success')
        return redirect(url_for('games.index'))

    return render_template('games/edit_game.html', title='Edit Game', game=game,
                           platforms=PLATFORMS, genres=GENRES, statuses=STATUSES)

@games_bp.route('/delete/<int:id>')
@login_required
def delete_game(id):
    game = db.session.get(Game, id)
    if not game or game.user_id != current_user.id:
        flash('Game not found.', 'danger')
        return redirect(url_for('games.index'))

    db.session.delete(game)
    db.session.commit()
    flash(f'Game "{game.title}" has been deleted.', 'success')
    return redirect(url_for('games.index'))

@games_bp.route('/search')
@login_required
def search():
    return render_template('games/search.html', title='Search Games')

@games_bp.route('/api/search')
@login_required
def api_search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])
    query = db.select(Game).where(
        Game.user_id == current_user.id,
        Game.title.ilike(f'%{q}%')
    )
    games = db.session.scalars(query).all()
    results = []
    for g in games:
        results.append({
            'id': g.id,
            'title': g.title,
            'platform': g.platform or '',
            'genre': g.genre or '',
            'status': (g.status or '').replace('_', ' ').title(),
            'status_raw': g.status or '',
            'rating': g.rating,
            'image_url': g.image_url or '',
            'note': g.note or ''
        })
    return jsonify(results)

