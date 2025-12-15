import logging
from motopp import db
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Part, UserPart

market = Blueprint('market', __name__)


def insert_user_part(user_id, part_id, type):
    up = UserPart(user_id=user_id, part_id=part_id, type=type)
    db.session.add(up)
    db.session.commit()
    logging.info(f"{current_user} {type} {part_id}")


@market.route('/market', methods=['GET', 'POST'])
@login_required
def marketPage():
    liked_parts = UserPart.query.filter_by(user_id=current_user.id).all()
    parts = Part.query.filter(Part.id.notin_([p.part_id for p in liked_parts])).limit(5).all()
    if request.method == 'POST':
        if request.form.get('liked'):
            insert_user_part(current_user.id, request.form.get('liked'), 'like')
        elif request.form.get('disliked'):
            insert_user_part(current_user.id, request.form.get('disliked'), 'dislike')
    return render_template('marketplace_test.html', parts=parts)

