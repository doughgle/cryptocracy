import os

from flask import Flask, request, flash, jsonify

from key_authority.ka_service.db import get_db
from . import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'ka_service.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        __version__ = '0.1.0'
        return 'Cryptocracy Key Authority Service (v%s)' % __version__

    # register directly with the app. TODO: later can be factored out into a blueprint.
    @app.route('/register', methods=('GET', 'POST'))
    def register():
        json_data = request.get_json()
        user_id = json_data['user_id']
        db = get_db()
        error = None
        if request.method == 'POST':
            if db.execute('SELECT id FROM user WHERE user_id = ?',
                          (user_id,)
                          ).fetchone() is not None:
                error = 'User {} is already registered.'.format(user_id)

            if not error:
                user_public_key = json_data['user_public_key']
                db.execute('INSERT INTO user (user_id, user_public_key) VALUES (?, ?)',
                           (user_id, user_public_key)
                           )
                db.commit()
            else:
                flash(error)

        user = db.execute('SELECT user_id, user_public_key FROM user WHERE user_id = ?',
                          (user_id,)
                          ).fetchone()

        return jsonify(user_id=user_id,
                       user_public_key=user['user_public_key'],
                       error=error)

    db.init_app(app)
    return app


