from flask import Blueprint
code_editor_bp = Blueprint('code_editor_bp', __name__)
from app.code_editor import routes