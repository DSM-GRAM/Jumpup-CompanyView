from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import config as cf
import logger


def _factory():
    """
    Creates Flask instance & initialize

    Flask best practice : Application Factories
    - Use 'application factory', 'current_app'

    :rtype: Flask
    """
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    CORS(app)
    JWTManager(app)

    logger.decorate(app)

    from blueprints import all_blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    return app

_app = _factory()


if __name__ == '__main__':
    _app.run(port=cf.PORT, threaded=True, debug=True)
