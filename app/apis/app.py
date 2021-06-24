from flask import Flask
from flask_cors import CORS
from app.apis.routers.cran_index_api import cran_index_bp


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
app.register_blueprint(cran_index_bp, url_prefix="/api/packages")
