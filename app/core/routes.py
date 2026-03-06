from flask import Blueprint, render_template, request
from app.extension import db
from app.models import Game
from flask_login import current_user, login_required


core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
    if current_user.is_authenticated:
        total = db.session.scalar(
            db.select(db.func.count(Game.id)).where(Game.user_id == current_user.id)
        ) or 0
        playing = db.session.scalar(
            db.select(db.func.count(Game.id)).where(Game.user_id == current_user.id, Game.status == 'playing')
        ) or 0
        completed = db.session.scalar(
            db.select(db.func.count(Game.id)).where(Game.user_id == current_user.id, Game.status == 'completed')
        ) or 0
        want_to_play = db.session.scalar(
            db.select(db.func.count(Game.id)).where(Game.user_id == current_user.id, Game.status == 'want_to_play')
        ) or 0
        dropped = db.session.scalar(
            db.select(db.func.count(Game.id)).where(Game.user_id == current_user.id, Game.status == 'dropped')
        ) or 0
        recent_games = db.session.scalars(
            db.select(Game).where(Game.user_id == current_user.id).order_by(Game.created_at.desc()).limit(5)
        ).all()
        return render_template('core/index.html', title='Dashboard',
                               total=total, playing=playing, completed=completed,
                               want_to_play=want_to_play, dropped=dropped,
                               recent_games=recent_games)
    return render_template('core/index.html', title='Welcome')

