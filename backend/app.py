from flask import Flask
from flask_cors import CORS

from .registration_login import registration_login_bp

import models

# Create Flask application
app = Flask(__name__)

models.init_db()

# Allow CORS for all origins
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8501"}})

#Register user and login
app.register_blueprint(registration_login_bp)

if __name__ == "__main__":
    app.run(debug=True)