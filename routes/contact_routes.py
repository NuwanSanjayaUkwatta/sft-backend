from flask import Blueprint
from controllers.contact_controller import create_contact, get_all_contacts, get_contact, update_contact, delete_contact

contact_blueprint = Blueprint('contact_blueprint', __name__)

# Create routes with the blueprint
contact_blueprint.route('/create', methods=['POST'])(create_contact)
contact_blueprint.route('/all', methods=['GET'])(get_all_contacts)
contact_blueprint.route('/get/<id>', methods=['GET'])(get_contact)
contact_blueprint.route('/update/<id>', methods=['PUT'])(update_contact)
contact_blueprint.route('/delete/<id>', methods=['DELETE'])(delete_contact)