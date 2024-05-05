from flask import Blueprint
from controllers.ai_controller import image_upload, train, predict

ai_blueprint = Blueprint('ai_blueprint', __name__)

# Create routes with the blueprint
ai_blueprint.route('/upload/<employee_id>', methods=['POST'])(image_upload)
ai_blueprint.route('/train', methods=['POST'])(train)
ai_blueprint.route('/predict', methods=['POST'])(predict)
