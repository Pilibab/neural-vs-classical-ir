from flask import Flask
from flask_cors import CORS # Add this
from config import settings
from api.routes.search import search_bp
from api.routes.manhwa import manhwa_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": f"{settings.frontend_url}"}})


# Tell Flask to use the routes defined in search.py
app.register_blueprint(search_bp)
app.register_blueprint(manhwa_bp)

@app.route("/")
def hello_world():
    print(settings.frontend_url)
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    # Set host='0.0.0.0' to make the server externally available (useful for testing across networks)
    # The default port is 5000
    app.run(
        debug=True,
        host='0.0.0.0',
        port=settings.port
        )