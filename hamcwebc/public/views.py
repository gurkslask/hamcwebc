# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from hamcwebc.extensions import login_manager
from hamcwebc.public.forms import LoginForm
from hamcwebc.user.forms import RegisterForm
from hamcwebc.user.models import User
from hamcwebc.utils import flash_errors
from hamcwebc.tasks import add_together, connect_to_pi
from hamcwebc.database import Sensor

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/home.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data, password=form.password.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)


@blueprint.route('/celery/')
def celery():
    """Celery page."""
    return(str(add_together.delay(1, 2)))


@blueprint.route('/connect/')
def connect():
    """Page for connecting to the pi."""
    return(str(connect_to_pi.delay({'r': ['VS1_GT1']})))


@blueprint.route('/connectSQL/')
def connectsql():
    """Page for showing data from SQL."""
    data = Sensor.query.filter_by(name='VS1_GT2').first()
    # data = Sensor.query.filter_by(name='VS1_GT1').first()
    print(data)
    print(type(data))
    if data:
            return(data.value())
    else:
            return render_template('404.html')
