from typing import TYPE_CHECKING
from flask import Flask
from flask_cors import CORS
from app.apis.routers.cran_index_api import cran_index_bp
from flask.json import JSONEncoder
from datetime import datetime


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app.json_encoder = CustomJSONEncoder

app.register_blueprint(cran_index_bp, url_prefix="/api/packages")
