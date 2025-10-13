from flask import Blueprint

bp = Blueprint("api_v1", __name__)

# ONLY users routes
from . import users  # noqa: E402,F401
from . import cfd  # noqa: E402,F401
