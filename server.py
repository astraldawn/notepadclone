from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os
import sqlite3
import string
import random

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'


def post_id_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/')
def show_entries():
    return redirect(post_id_generator())
    # db = get_db()
    # cur = db.execute('SELECT title, text FROM entries ORDER BY id DESC')
    # entries = cur.fetchall()
    # return render_template('show_entries.html', entries=entries)


# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     # Use ? ? to prevent SQL injection
#
#     # TODO: Strip the content in the 'text' field
#     db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
#                [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     """Storing as plaintext for simplicity now, Werkzeug has security helpers"""
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)
#
#
# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))


@app.route('/<string:post_id>')
def show_post(post_id):
    """A page for a new post"""
    if not validate_post(post_id):
        abort(404)

    content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam tortor velit, gravida nec dui id, " \
              "venenatis malesuada nunc. Nullam bibendum, arcu fermentum fermentum sagittis, ligula enim rhoncus " \
              "nulla, quis commodo eros nibh quis arcu. Nunc dignissim lacus eu molestie auctor. Duis erat quam, " \
              "scelerisque non viverra sit amet, gravida eget lectus. Maecenas egestas urna non gravida gravida. Cras " \
              "quis tortor at massa vulputate blandit. Nunc aliquam, ipsum sit amet dignissim scelerisque, " \
              "ligula diam volutpat tortor, molestie condimentum nisl massa quis nisi. Mauris non gravida nulla. " \
              "Vestibulum a leo cursus, mollis tortor at, ultricies eros. Nulla posuere, mauris a pretium feugiat, " \
              "ante arcu porta erat, in auctor leo ipsum quis eros. Aenean turpis urna, rhoncus eu placerat quis, " \
              "imperdiet sit amet tortor. Phasellus rhoncus orci quis nisi faucibus luctus. Curabitur ut metus justo. " \
              "Morbi eget cursus turpis, eget lobortis ex. Aliquam id elit lacinia, ullamcorper quam sit amet, " \
              "placerat elit. Curabitur scelerisque libero et maximus porttitor. Suspendisse potenti. Fusce " \
              "ullamcorper iaculis condimentum. Vestibulum dignissim molestie volutpat. Suspendisse potenti. Donec " \
              "non interdum augue. Morbi venenatis sagittis augue vitae pellentesque. Maecenas non consequat odio. " \
              "Pellentesque semper, ante at efficitur vestibulum, sapien libero mollis enim, et commodo arcu nisi in " \
              "nibh. Duis tristique aliquam consectetur. Vestibulum volutpat sapien quis turpis pretium accumsan ut " \
              "nec sem. Sed ultricies ornare felis ut commodo. Maecenas hendrerit leo eu nisi condimentum, " \
              "in finibus libero mollis. Nullam erat elit, dignissim vitae sodales vel, congue posuere nulla. Nunc a " \
              "euismod augue. Vivamus et arcu risus. Praesent vehicula libero eget mi pulvinar, sed condimentum purus " \
              "vulputate. Integer sed interdum velit. Curabitur euismod felis metus, vitae dignissim sem viverra " \
              "eget. Nunc fringilla, odio sit amet iaculis consectetur, arcu erat efficitur nisl, eget ultricies " \
              "augue turpis non nunc.Suspendisse nec rutrum dolor. Curabitur vulputate enim ultrices ligula iaculis, " \
              "a porttitor lectus porttitor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere " \
              "cubilia Curae; Nulla rutrum sollicitudin justo, ornare convallis tortor ornare eget. Maecenas " \
              "fringilla leo porta sapien semper facilisis. Phasellus urna orci, lobortis quis ex non, sollicitudin " \
              "consequat nulla. Aenean nec mauris quam. Phasellus vitae auctor est. Cras elit nulla, laoreet vel " \
              "felis in, laoreet pulvinar urna. Quisque dictum accumsan turpis, sit amet iaculis orci porttitor quis. " \
              "Nulla tincidunt ornare placerat. Nam porta nisl a elit mollis lacinia. "
    return render_template('layout.html', content=content, post_id=post_id, word_count=0, lines=0)


def validate_post(post_id):
    if len(post_id) != 8:
        return False
    return True


if __name__ == "__main__":
    app.run()
