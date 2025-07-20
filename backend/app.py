from flask import Flask
from flask_cors import CORS
from config import Config
from mongoengine import connect
from routes.image_routes import image_bp

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for all origins (React frontend can access)
CORS(app)

# Connect to MongoDB
connect(host=app.config['MONGO_URI'])
print("Connected to MongoDB.")

# Register routes
app.register_blueprint(image_bp, url_prefix='/api/images')

# Run Flask server on port from .env
if __name__ == '__main__':
    print(f"Server running on port {app.config['FLASK_PORT']}")
    app.run(debug=True, port=app.config['FLASK_PORT'],host="0.0.0.0")
