from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os
from routes.employee_routes import employee_blueprint
from routes.ai_routes import ai_blueprint
from routes.attendance_routes import attendance_blueprint
from routes.admin_routes import admin_blueprint
from routes.contact_routes import contact_blueprint

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configurations
app.config['MONGODB_SETTINGS'] = {
    'db': os.environ.get('MONGO_DB_NAME'),  # Retrieve database name from .env
    'host': os.environ.get('MONGO_URI')
}
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET')


db = MongoEngine(app)
CORS(app)

app.register_blueprint(employee_blueprint, url_prefix='/api/employees')
app.register_blueprint(ai_blueprint, url_prefix='/api/ai')
app.register_blueprint(attendance_blueprint, url_prefix='/api/attendance')
app.register_blueprint(admin_blueprint, url_prefix='/api/admin')
app.register_blueprint(contact_blueprint, url_prefix='/api/contact')

@app.route('/')
def index():
    return "API is running..."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3001)), debug=True)