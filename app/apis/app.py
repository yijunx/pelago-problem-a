from flask import Flask
from flask_cors import CORS
from app.apis.routers.cran_index_api import photo_bq


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
app.register_blueprint(photo_bq, url_prefix="/api/photos")
