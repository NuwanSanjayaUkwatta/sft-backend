from mongoengine import Document, StringField, EmailField, IntField

class Contact(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    phone = IntField(required=True)
    message = StringField(required=True)