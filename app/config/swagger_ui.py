from flask import Blueprint, send_from_directory
import os

swagger_ui_bp = Blueprint('swagger_ui', __name__)

@swagger_ui_bp.route('/docs')
def swagger_ui():
    return send_from_directory('static', 'swagger.html')

@swagger_ui_bp.route('/swagger.yaml')
def swagger_yaml():
    return send_from_directory('static', 'swagger.yaml') 