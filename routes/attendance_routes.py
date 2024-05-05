from flask import Blueprint
from controllers.attendance_controller import mark, edit, get_all_attendance

attendance_blueprint = Blueprint('attendance_blueprint', __name__)

# Define routes with the blueprint
attendance_blueprint.route('/mark', methods=['POST'])(mark)
attendance_blueprint.route('/update/<attendance_id>', methods=['PUT'])(edit)
attendance_blueprint.route('/all', methods=['GET'])(get_all_attendance)
