from mongoengine import Document, ReferenceField, StringField
from models.employee import Employee

class Attendance(Document):
    employee = ReferenceField(Employee, required=True)
    date = StringField(required=True)  # Changed from DateTimeField to StringField
    time = StringField(required=True)  # Added time field
    status = StringField(required=True, choices=('present', 'absent', 'late'), default='present')