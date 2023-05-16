from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from redis import Redis
import rq

from config import Config

import uuid


def fk_guid(constraint, table):
    str_tokens = [
        table.name,
    ] + [
        element.parent.name for element in constraint.elements
    ] + [
        element.target_fullname for element in constraint.elements
    ]
    guid = uuid.uuid5(uuid.NAMESPACE_OID, "_".join(str_tokens))
    return str(guid)


convention = {
    "fk_guid": fk_guid,
    "ix": 'ix_%(column_0_label)s',
    "fk": "fk_%(fk_guid)s",
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('ativagrid-tasks', connection=app.redis, default_timeout=36000)

    from app import models

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


    return app
