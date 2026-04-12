# auth/__init__.py
from flask import Blueprint

# Blueprint name, import name, URL prefix
mft_AuthBP = Blueprint(
    "auth", # Internal name
    __name__, # Import name tells Flask where to find templates/static
    url_prefix="/", # all routes will be prefixed with /
    template_folder="templates", # Defaults to src/templates
)

# Import routes after the blueprint is created to avoid circular imports
from . import routes
