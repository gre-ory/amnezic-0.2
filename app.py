# ##################################################
# import

import flask

import lib.sql
import lib.db
import lib.theme
import lib.track

import lib.plugin.deezer

# ##################################################
# config

DEBUG = True
TESTING = False
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = ''

# ##################################################
# app

app = flask.Flask('amnezic')
app.config.from_object(__name__)
app.db = lib.sql.Database(lib.db.FILE)


# ##################################################
# db

@app.before_request
def before_request():
    lib.plugin.source = lib.plugin.deezer.source
    app.db.connect()


@app.teardown_request
def teardown_request(exception):
    app.db.commit()
    app.db.disconnect()


@app.route('/db/reset')
def init_db():
    # if not session.get( 'logged_in' ):
    #    abort( 401 )
    app.db.execute_file(lib.db.SCHEMA)
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
    if flask.request.method == 'POST':
        if flask.request.form['username'] != username:
            error = ERROR_INVALID_USER
        elif flask.request.form['password'] != password:
            error = ERROR_INVALID_PASSWORD
        else:
            flask.session['logged_in'] = True
            flask.flash(SUCCESS_LOGIN)
            return flask.redirect(flask.url_for('track_list'))
    return flask.render_template('login.html', error=error)


@app.route('/logout')
def logout():
    flask.session.pop('logged_in', None)
    flask.flash(SUCCESS_LOGOUT)
    return flask.redirect(flask.url_for('login'))


# ##################################################
# theme

SUCCESS_THEME_LIST_EMPTY = 'no theme'
SUCCESS_THEME_CREATE = 'track was successfully create'
SUCCESS_THEME_UPDATE = 'track was successfully updated'
SUCCESS_THEME_DELETE = 'track was successfully deleted'


@app.route('/')
@app.route('/theme')
def theme_retrieve_all():
    themes = lib.theme.retrieve_all()
    len(themes) != 0 or flask.flash(SUCCESS_THEME_LIST_EMPTY)
    return flask.render_template('theme.html', themes=themes)


@app.route('/theme/<oid>')
def theme_retrieve(oid):
    theme = lib.theme.retrieve(oid)
    return flask.render_template('theme.html', theme=theme)


@app.route('/theme/<oid>/add/<track_oid>', methods=['GET'])
def theme_add_track(oid, track_oid):
    lib.track.add_theme(track_oid, oid)
    theme = lib.theme.add_track(oid, track_oid)
    flask.flash(SUCCESS_THEME_UPDATE)
    return flask.render_template('theme.html', theme=theme)


@app.route('/theme/<oid>/remove/<track_oid>', methods=['GET'])
def theme_remove_track(oid, track_oid):
    lib.track.remove_theme(track_oid, oid)
    theme = lib.theme.remove_track(oid, track_oid)
    flask.flash(SUCCESS_THEME_UPDATE)
    return flask.render_template('theme.html', theme=theme)


@app.route('/theme/delete/<oid>')
def theme_delete(oid):
    lib.theme.delete(oid)
    flask.flash(SUCCESS_THEME_DELETE)
    return flask.redirect(flask.url_for('theme_retrieve_all'))


# ##################################################
# track

SUCCESS_TRACK_LIST_EMPTY = 'no track'
SUCCESS_TRACK_CREATE = 'track was successfully create'
SUCCESS_TRACK_UPDATE = 'track was successfully updated'
SUCCESS_TRACK_DELETE = 'track was successfully deleted'


@app.route('/track/search', methods=['POST'])
def track_search():
    tracks = lib.track.search(query=flask.request.form['query'])
    return flask.render_template('track.html', tracks=tracks, query=flask.request.form['query'])


@app.route('/track/view/<oid>')
def track_view(oid):
    track = lib.track.search(oid=oid)
    print track.indented_json
    return flask.render_template('track.html', track=track)


@app.route('/track')
def track_retrieve_all():
    tracks = lib.track.retrieve_all()
    len(tracks) != 0 or flask.flash(SUCCESS_TRACK_LIST_EMPTY)
    return flask.render_template('track.html', tracks=tracks)


@app.route('/track/<oid>')
def track_retrieve(oid):
    track = lib.track.retrieve(oid)
    return flask.render_template('track.html', track=track)


@app.route('/track/add/<oid>', methods=['GET'])
def track_add(oid):
    track = lib.track.create(oid)
    flask.flash(SUCCESS_TRACK_CREATE)
    return flask.render_template('track.html', track=track)


@app.route('/track/update/<oid>', methods=['GET'])
def track_update(oid):
    track = lib.track.upsert(oid)
    flask.flash(SUCCESS_TRACK_UPDATE)
    return flask.render_template('track.html', track=track)


@app.route('/track/delete/<oid>')
def track_delete(oid):
    lib.track.delete(oid)
    flask.flash(SUCCESS_TRACK_DELETE)
    return flask.redirect(flask.url_for('track_retrieve_all'))


if __name__ == '__main__':
    app.run(host=None, port=8042)
