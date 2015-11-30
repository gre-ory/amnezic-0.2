# ##################################################
# import

from flask import Flask, request, session, redirect, url_for, render_template, flash
from lib import track
from lib import sql
from lib import db
from lib.plugin import deezer

# ##################################################
# config

DEBUG = True
TESTING = False
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = ''

# ##################################################
# app

app = Flask('amnezic')
app.config.from_object(__name__)
app.db = sql.Database(db.FILE)


# ##################################################
# db

@app.before_request
def before_request():
    track.source = deezer.source
    app.db.connect()


@app.teardown_request
def teardown_request():
    app.db.commit()
    app.db.disconnect()


@app.route('/db/reset')
def init_db():
    # if not session.get( 'logged_in' ):
    #    abort( 401 )
    app.db.execute_file(db.SCHEMA)
    return 'OK'


# ##################################################
# login

ERROR_INVALID_USER = 'Invalid username'
ERROR_INVALID_PASSWORD = 'Invalid password'
SUCCESS_LOGIN = 'You were logged in'
SUCCESS_LOGOUT = 'You were logged out'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    username = app.config['USERNAME'] if not app.config['TESTING'] else 'test'
    password = app.config['PASSWORD'] if not app.config['TESTING'] else 'test'
    if request.method == 'POST':
        if request.form['username'] != username:
            error = ERROR_INVALID_USER
        elif request.form['password'] != password:
            error = ERROR_INVALID_PASSWORD
        else:
            session['logged_in'] = True
            flash(SUCCESS_LOGIN)
            return redirect(url_for('track_list'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(SUCCESS_LOGOUT)
    return redirect(url_for('login'))


# ##################################################
# track

SUCCESS_TRACK_LIST_EMPTY = 'no track'
SUCCESS_TRACK_CREATE = 'track was successfully create'
SUCCESS_TRACK_UPDATE = 'track was successfully updated'
SUCCESS_TRACK_DELETE = 'track was successfully deleted'


@app.route('/')
@app.route('/track')
def track_retrieve_all():
    items = track.retrieve_all()
    if len(items) == 0:
        flash(SUCCESS_TRACK_LIST_EMPTY)
    return render_template('track.html', tracks=items)


@app.route('/track/search', methods=['POST'])
def track_search():
    items = track.search(request.form['query'])
    return render_template('track.html', tracks=items)


@app.route('/track/<id>')
def track_retrieve(id):
    print id
    item = track.retrieve(id)
    print item
    return render_template('track.html', track=item)


@app.route('/track/add/<deezer_id>', methods=['GET'])
def track_add(deezer_id):
    # if not session.get( 'logged_in' ):
    #    abort( 401 )
    item = track.create(deezer_id)
    flash(SUCCESS_TRACK_CREATE)
    return redirect(url_for('track_retrieve', id=item.id))


@app.route('/track/update/<oid>', methods=['GET'])
def track_update(oid):
    item = track.delete(oid)
    item = track.create(item.deezer_id)
    flash(SUCCESS_TRACK_UPDATE)
    return redirect(url_for('track_retrieve', id=item.id))


@app.route('/track/create', methods=['POST'])
def track_create():
    # if not session.get( 'logged_in' ):
    #    abort( 401 )
    item = track.create(request.form['deezer_id'])
    flash(SUCCESS_TRACK_CREATE)
    return redirect(url_for('track_retrieve', id=item.id))


@app.route('/track/delete/<id>')
def track_delete(id):
    item = track.delete(id)
    flash(SUCCESS_TRACK_DELETE)
    return redirect(url_for('track_retrieve_all'))


if __name__ == '__main__':
    app.run(host=None, port=8042)
