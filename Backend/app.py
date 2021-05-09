import os
from flask import Flask, json,jsonify,request
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,JWTManager
from flask_cors import CORS
from flask_mysqldb import MySQL
import pymongo
from werkzeug.security import generate_password_hash,check_password_hash
import yaml

# Mongodb Atlas DB .
connection_url = 'mongodb+srv://kapil:kkkk@predictsportcluster.t4020.mongodb.net/predictsportdb?retryWrites=true&w=majority'
app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient(connection_url)
  
# Database
Database = client.get_database('predictsportdb')
# Table
UserTable = Database['_user']
PerdictionTable = Database['_prediction']
sample_user = UserTable.find_one({
    'username':'test_user'
})
print(sample_user['password'])
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
def index():
    return jsonify("index")

## register a user
@app.route('/register',methods=['POST'])
def register(): 
    res = None
    ## get user details from request
    user_details = request.get_json()
    username = user_details['username']
    password = user_details['password']
    score = 0

    ## if there is no user with same username then register user with initial score as 0
    existing_user = UserTable.find_one({'username':username})
    if existing_user is None:
        new_user_object = {
            'username': username,
            'password': generate_password_hash(password),
            'score': score
        }
        UserTable.insert_one(new_user_object)
        res = {
            'msg':'Successfully registered',
            'status': 200
        }
    else:
        res = {
            'msg': 'username taken',
            'status': 409
        }
    
    return jsonify(res)

## login a user
@app.route('/login',methods=['POST'])
def login():
    res = None
    ## get details from request
    userdetails = request.get_json()
    username_in = userdetails['username']
    password_in = userdetails['password']

    ## find if a user with given username and password exists if yes then create jwt and return success response else return fail response
    user_search = UserTable.find_one({
        'username':username_in,
    })
    if user_search is not None and check_password_hash(user_search['password'],password_in):
        access_token = create_access_token(identity=username_in)
        res = {
            'msg': 'Login successfull',
            'access-token': access_token,
            'status': 200
        }
    else:
        res = {
            'msg': 'Invalid credentials',
            'status': 401
        }
    
    return jsonify(res)

## logout user
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

@app.route('/makeprediction',methods=['POST'])
@jwt_required()
def postPrediction():
    if request.method == 'POST':
        username = get_jwt_identity()
        req = request.get_json()
        matchid = req['matchid']
        prediction = req['prediction']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO prediction (matchid,username,prediction) VALUES (%s,%s,%s)",(matchid,username,prediction))
        mysql.connection.commit()
        return jsonify({
            "msg":"Prediction added successfully",
            "status":200
        })

@app.route('/getpredictions',methods=['GET'])
def getPredictions():
    cur = mysql.connection.cursor()
    n_predictions = cur.execute("SELECT * FROM predictions")
    if n_predictions > 0:
        resp = cur.fetchall()
        result = []
        obj = {}
        for prediction in resp:
            obj = {
                "matchid":prediction[0],
                "username":prediction[1],
                "prediction":prediction[2]
            }
            result.append(obj)
            obj = {}
        return jsonify({
            "msg":"Predictions fetched successfully",
            "data": result,
            "number of predictions":n_predictions,
            "status":200
        })
    else:
        return jsonify({
            "msg":"No Predictions to fetch",
            "data": "",
            "number of predictions":n_predictions,
            "status":404
        })

@app.route('/getpredictions/<string:username>',methods=['GET'])
@jwt_required()
def getPredictions_by_username(username):
    cur = mysql.connection.cursor()
    n_predictions = cur.execute("SELECT * FROM predictions WHERE username=%s",(username,))
    if n_predictions > 0:
        resp = cur.fetchall()
        result = []
        obj = {}
        for prediction in resp:
            obj = {
                "matchid":prediction[0],
                "username":prediction[1],
                "prediction":prediction[2]
            }
            result.append(obj)
            obj = {}
        return jsonify({
            "msg":"Predictions fetched successfully",
            "data": result,
            "number of predictions":n_predictions,
            "status":200
        })
    else:
        return jsonify({
            "msg":"No Predictions to fetch",
            "data": "",
            "number of predictions":n_predictions,
            "status":404
        })

@app.route('/getpredictions/<string:matchid>',methods=['GET'])
@jwt_required()
def getPredictions_by_match(matchid):
    cur = mysql.connection.cursor()
    n_predictions = cur.execute("SELECT * FROM predictions WHERE matchid=%s",(matchid,))
    if n_predictions > 0:
        resp = cur.fetchall()
        result = []
        obj = {}
        for prediction in resp:
            obj = {
                "matchid":prediction[0],
                "username":prediction[1],
                "prediction":prediction[2]
            }
            result.append(obj)
            obj = {}
        return jsonify({
            "msg":"Predictions fetched successfully",
            "data": result,
            "number of predictions":n_predictions,
            "status":200
        })
    else:
        return jsonify({
            "msg":"No Predictions to fetch",
            "data": "",
            "number of predictions":n_predictions,
            "status":404
        })

@app.route('/getpredictions/<string:username>/<string:matchid>',methods=['GET'])
@jwt_required()
def getPrediction(username,matchid):
    cur = mysql.connection.cursor()
    n_predictions = cur.execute("SELECT * FROM predictions WHERE username=%s AND matchid=%s",(username,matchid))
    if n_predictions > 0:
        resp = cur.fetchall()
        result = []
        obj = {}
        for prediction in resp:
            obj = {
                "matchid":prediction[0],
                "username":prediction[1],
                "prediction":prediction[2]
            }
            result.append(obj)
            obj = {}
        return jsonify({
            "msg":"Predictions fetched successfully",
            "data": result,
            "number of predictions":n_predictions,
            "status":200
        })
    else:
        return jsonify({
            "msg":"No Predictions to fetch",
            "data": "",
            "number of predictions":n_predictions,
            "status":404
        })

@app.route('/user/<string:username>',methods=['POST'])
def update_score(username):
    req = request.get_json()
    score = req['score']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE username=%s",(username,))
    n_user = cur.fetchone()
    if n_user>0:
        cur.execute("UPDATE user SET score=%s WHERE username=%s",(score,username))
        mysql.connection.commit()
        return jsonify({
            "msg":"Score updated successfully",
            "status":200
        })
    else:
        return jsonify({
            "msg":"Username not found",
            "status":404
        })

if __name__ == '__main__':
    app.run(debug=True)