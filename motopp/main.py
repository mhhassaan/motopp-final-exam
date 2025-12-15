from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .forms import AddBikeForm
from .models import Bike
from . import db
import logging

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/mybikes')
@login_required
def mybikes():
    bikes = current_user.bikes
    return render_template('mybikes.html', name=current_user.name, bikes=bikes)


@main.route('/add_bike', methods=['GET', 'POST'])
@login_required
def add_bike():
    form = AddBikeForm()
    if form.validate_on_submit():
        bike = Bike(name=form.name.data, make=form.make.data, model=form.model.data, year=form.year.data,
                    user_id=current_user.id)
        db.session.add(bike)
        db.session.commit()
        logging.info(f"Bike added: {bike.name}")
        return redirect(url_for('main.mybikes'))
    return render_template('add_bike.html', form=form)
