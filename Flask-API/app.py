import os
from flask import Flask, json,jsonify,request
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,JWTManager
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash,check_password_hash
import yaml
app = Flask(__name__, instance_relative_config=True)

keys = yaml.load(open('./keys/keys.yaml'))

##configure app
app.config.from_mapping(
    SECRET_KEY='dev'
)

mysql = MySQL()
app.config['MYSQL_HOST'] = keys['mysql_host']
app.config['MYSQL_USER'] = keys['mysql_user']
app.config['MYSQL_PASSWORD'] = keys['mysql_password']
app.config['MYSQL_DB'] = keys['mysql_db']
mysql.init_app(app)

app.config["JWT_SECRET_KEY"] = keys['jwt_key']
jwt = JWTManager(app)    

@app.route('/')
@jwt_required()
def index():
    return jsonify("index")

@app.route('/register',methods=['POST'])
def register(): 
    user_details = request.get_json()
    username = user_details['username']
    password = user_details['password']
    score = user_details['score']
    cur = mysql.connection.cursor()
    n_user = cur.execute("SELECT * FROM user WHERE username=%s",(username,))
    if n_user>0:
        return jsonify({
            "msg":"Username already taken",
            "status":409
        })
    else:
        cur.execute("INSERT INTO user (username,password,score) VALUES (%s,%s,%s)",(username,generate_password_hash(password),score))
        mysql.connection.commit()
    return jsonify({
        "msg":"user successfully registered",
        "status":200,
        "data":user_details
    })

@app.route('/login',methods=['POST'])
def login():
    incorrect_return_object = {
        "msg":"username or password incorrect",
        "status":403
    }
    userdetails = request.get_json()
    username = userdetails['username']
    password = userdetails['password']
    cur = mysql.connection.cursor()
    n_user = cur.execute('SELECT * FROM user WHERE username=%s',(username,))
    if n_user>0:
        db_user = cur.fetchone()
        hashed_password = db_user[1]
        if check_password_hash(hashed_password,password):
            access_token = create_access_token(identity=username)
            correct_return_object = {
                "msg":"Successfully logged in",
                "status":200,
                "access-token":access_token
            }
            return jsonify(correct_return_object)
        else:
            return jsonify(incorrect_return_object)
    else :
        return jsonify(incorrect_return_object)

@app.route('/logout',methods=['GET'])
@jwt_required()
def logout():
    username = get_jwt_identity()
    return jsonify({
        "msg":"Successfully logged out",
        "status":200,
        "data":{
            "username":username
        }
    })

if __name__ == '__main__':
    app.run(debug=True)