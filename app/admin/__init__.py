from flask import Blueprint

movie = Blueprint('movie',__name__)

from . import views