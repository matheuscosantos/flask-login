from flask_login import login_user, login_required, current_user
from werkzeug.utils import redirect

from app import app, db
from flask import render_template, flash, url_for, session, request, g, jsonify

from app.models.forms import LoginForm, CreateUserForm
from app.models.tables import User


@app.route("/index/<user>")
@app.route("/", defaults={"user": None})
def index(user):
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('timeline'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        session.pop('user', None)
        if user and user.password == form.password.data:
            login_user(user)
            flash("Logged in.")
            return redirect(url_for('timeline'))
        else:
            flash("Invalid login.")
    else:
        print(form.errors)
    return render_template('login.html', form=form)


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    name=form.name.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You may now login.')
        return redirect(url_for('login'))
    else:
        print(form.errors)

    return render_template('subscribe.html', form=form, title='Subscribe')


@app.route('/timeline', methods=['GET'])
@login_required
def timeline():
    # if g.user:
    #     return render_template('timeline.html', user=session['user'])
    # return redirect(url_for('timeline'))
    return render_template('timeline.html')


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
