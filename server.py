from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os
import sqlite3
import string
import random
import json

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('SERVER_SETTINGS', silent=True)


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


# should combine show and save into a single route
@app.route('/<string:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    """A page for a new post as well as for saving a post"""
    if request.method == 'POST':
        print "POST: ", post_id, request.form
        db = get_db()

        data = [(post_id,
                 request.form['content'],
                 int(request.form['caretPos']),
                 int(request.form['scrollTop']),
                 int(request.form['fontSize'])
                 )]

        # Use ? ? to prevent SQL injection
        db.executemany(
            'INSERT OR REPLACE INTO posts VALUES (?, ?, ?, ?, ?)', data
        )

        db.commit()

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    if not validate_post(post_id):
        abort(404)

    db = get_db()
    cur = db.execute('SELECT * FROM posts WHERE id=:id', {"id": post_id})
    entries = cur.fetchall()

    print "GET: ", entries, len(entries)

    content = ""
    caret_pos = 0
    scroll_top = 0
    font_size = 15

    if entries:
        content = entries[0][1]
        caret_pos = entries[0][2]
        scroll_top = entries[0][3]
        font_size = entries[0][4]

    return render_template('layout.html',
                           content=content,
                           postID=post_id,
                           caretPos=caret_pos,
                           scrollTop=scroll_top,
                           fontSize=font_size)


def validate_post(post_id):
    if len(post_id) != 8:
        return False
    return True


if __name__ == "__main__":
    app.run()
