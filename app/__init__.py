import os
from flask import Flask
from sqlalchemy import inspect
from .config import Config
from .extensions import db
from .utils.responses import not_found as _not_found, bad_request as _bad_request, server_error as _server_error
from .models import register_models

def create_app(config_object: type[Config] | None = None):
    app = Flask(__name__)
    app.config.from_object(config_object or Config)

    # DB init
    db.init_app(app)

    # Reflect metadata then register ONLY the users model
    with app.app_context():
        schema = app.config.get("DB_SCHEMA")
        db.Model.metadata.reflect(bind=db.engine, schema=schema, views=True)

        # (optional) quick visibility while setting up; comment out later
        insp = inspect(db.engine)
        print("Schemas:", insp.get_schema_names())
        print("Reflected tables:", list(db.Model.metadata.tables.keys()))

        register_models()

    @app.get("/")
    def health():
        return {"code": 200, "message": "OK", "data": {"service": "your_api", "env": os.getenv("FLASK_ENV", "unknown")}}

    @app.errorhandler(404)
    def _404(e): return _not_found("Endpoint not found")
    @app.errorhandler(400)
    def _400(e): return _bad_request("Bad request")
    @app.errorhandler(500)
    def _500(e): return _server_error("Unexpected server error")

    from .api.v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")

    return app
