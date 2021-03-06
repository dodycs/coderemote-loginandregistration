import re
from flask import Flask, session, request, redirect, render_template, flash, url_for
from db.data_layer import get_user_by_email, get_user_by_id, create_user

app = Flask(__name__)
app.secret_key = '8118d0875ad5b6b3ad830b956b111fb0'

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate')
def authenticate():
    return render_template('authenticate.html')


def is_blank(name, field):
    if len(field) == 0:
        flash('{} cannot be blank'.format(name))
        return True
    return False

@app.route('/register', methods=['POST'])
def register():
    fullname = request.form['html_fullname']
    email = request.form['html_email']
    password = request.form['html_password']
    confirm = request.form['html_confirm']

    is_valid = True

    is_valid = is_blank('Fullname', fullname)
    is_valid = is_blank('Email', email)
    is_valid = is_blank('Password', password)
    is_valid = is_blank('Confirm Password', confirm)

    if password != confirm:
        flash('Password do not match')
        is_valid = False
    if len(password) < 6:
        flash('Password have to be more than 6')
        is_valid = False
    if not EMAIL_REGEX.match(email):
        flash('Email format is wrong')
        is_valid = False

    if is_valid:
        try:
            user = create_user(email, fullname, password)
            session['name'] = user.name
            return redirect(url_for('index'))
        except:
            flash('Email alredy registered')
    return redirect(url_for('authenticate'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['html_email']
    password = request.form['html_password']

    try:
        user = get_user_by_email(email)
        if user.password == password:
            session['user_id'] = user.id
            session['user_name'] = user.email
            session['name'] = user.name
            return redirect(url_for('index'))
        else:
            flash('Password not match')
    except:
        raise
        flash('Login failed')
    return redirect(url_for('authenticate'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

app.run(debug=True)
