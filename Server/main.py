from flask import Flask
from flask_cors import CORS

import logger


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    CORS(app)

    logger.decorate(app)

    from blueprints import all_blueprints

    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)

    return app


_app = create_app()

if __name__ == '__main__':
    _app.run(host='localhost', port=_app.config['PORT'], threaded=True, debug=True)
