from flask import jsonify, request
from models.contact import Contact

def create_contact():
    data = request.json
    contact = Contact(**data)
    contact.save()
    return jsonify({"message": "Contact saved successfully", "id": str(contact.id)}), 200

def get_all_contacts():
    contacts = Contact.objects.all()
    if contacts:
        contacts_data = []
        for contact in contacts:
            contact_dict = {
                'id': str(contact.id),
                'name': contact.name,
                'email': contact.email,
                'phone': contact.phone,
                'message': contact.message,
            }
            contacts_data.append(contact_dict)
        return jsonify(contacts_data), 200
    else:
        return jsonify({"message": "No contacts found"}), 404

def get_contact(id):
    contact = Contact.objects(id=id).first()
    if contact:
        return jsonify({
            'id': str(contact.id),
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone,
            'message': contact.message,
        })
    else:
        return jsonify({"error": "Contact not found"}), 404

def update_contact(id):
    data = request.json
    contact = Contact.objects(id=id).first()
    if contact:
        contact.update(**data)
        return jsonify({"message": "Contact updated successfully"}), 200
    else:
        return jsonify({"error": "Contact not found"}), 404

def delete_contact(id):
    contact = Contact.objects(id=id).first()
    if contact:
        contact.delete()
        return jsonify({"message": "Contact deleted successfully"})
    else:
        return jsonify({"error": "Contact not found"}), 404