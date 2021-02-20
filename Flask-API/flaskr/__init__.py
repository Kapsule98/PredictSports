import os
from flask import Flask,jsonify
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,JWTManager

def create_app(test_config = None):
    #create app
    app = Flask(__name__, instance_relative_config=True)

    ##configure app
    app.config["JWT_SECRET_KEY"] = 'dev'
    app.config.from_mapping(
        SECRET_KEY='dev'
        ##db connection goes here
    )
    jwt = JWTManager(app)    

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return jsonify("index")

    return app