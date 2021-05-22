from flask import Flask, json,jsonify,request
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,JWTManager
from flask_cors import CORS
import pymongo
from werkzeug.security import generate_password_hash,check_password_hash
import http.client
import json
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

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


##configure app
app.config.from_mapping(
    SECRET_KEY='dev'
)



app.config["JWT_SECRET_KEY"] = 'dev'
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
        access_token = create_access_token(identity=username_in, expires_delta=False)
        res = {
            'msg': 'Login successfull',
            'accesstoken': access_token,
            'username': username_in,
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
def logout():
    return jsonify({
        "msg":"Successfully logged out",
        "status":200,
    })

@app.route('/user', methods=['GET'])
@jwt_required()
def getUsers():
    resData = UserTable.find()
    usersdata = []
    for user in resData:
        userobj = {
            'username': user['username'],
            'score': user['score']
        }
        usersdata.append(userobj)
    res = None
    if usersdata is not None:
        res = {
            'msg':'All users fetched',
            'data': usersdata,
            'status':200
        }
    else:
        res = {
            'msg':'No users found',
            'status': 404
        }
    return jsonify(res)

@app.route('/makeprediction',methods=['POST'])
@jwt_required()
def postPrediction():
    if request.method == 'POST':
        username = get_jwt_identity()
        req = request.get_json()
        matchid = req['matchid']
        prediction = req['prediction']
        matchObj = PerdictionTable.find_one({
            'matchid': matchid,
            'username':username
        })
        if matchObj is not None:
            selection_query = {
                'matchid': matchid,
                'username':username
            }
            new_values = {
                "$set": {
                    "prediction":prediction
                }
            }
            PerdictionTable.update_one(selection_query,new_values)

        else :
            PerdictionTable.insert_one({
                'matchid': matchid,
                'username':username,
                'prediction': prediction
            })

        return jsonify({
            "msg":"Prediction added successfully",
            "status":200
        })

# @app.route('/getpredictions',methods=['GET'])
# def getPredictions():
#     cur = mysql.connection.cursor()
#     n_predictions = cur.execute("SELECT * FROM predictions")
#     if n_predictions > 0:
#         resp = cur.fetchall()
#         result = []
#         obj = {}
#         for prediction in resp:
#             obj = {
#                 "matchid":prediction[0],
#                 "username":prediction[1],
#                 "prediction":prediction[2]
#             }
#             result.append(obj)
#             obj = {}
#         return jsonify({
#             "msg":"Predictions fetched successfully",
#             "data": result,
#             "number of predictions":n_predictions,
#             "status":200
#         })
#     else:
#         return jsonify({
#             "msg":"No Predictions to fetch",
#             "data": "",
#             "number of predictions":n_predictions,
#             "status":404
#         })

# @app.route('/getpredictions/<string:username>',methods=['GET'])
# @jwt_required()
# def getPredictions_by_username(username):
#     cur = mysql.connection.cursor()
#     n_predictions = cur.execute("SELECT * FROM predictions WHERE username=%s",(username,))
#     if n_predictions > 0:
#         resp = cur.fetchall()
#         result = []
#         obj = {}
#         for prediction in resp:
#             obj = {
#                 "matchid":prediction[0],
#                 "username":prediction[1],
#                 "prediction":prediction[2]
#             }
#             result.append(obj)
#             obj = {}
#         return jsonify({
#             "msg":"Predictions fetched successfully",
#             "data": result,
#             "number of predictions":n_predictions,
#             "status":200
#         })
#     else:
#         return jsonify({
#             "msg":"No Predictions to fetch",
#             "data": "",
#             "number of predictions":n_predictions,
#             "status":404
#         })

# @app.route('/getpredictions/<string:matchid>',methods=['GET'])
# @jwt_required()
# def getPredictions_by_match(matchid):
#     cur = mysql.connection.cursor()
#     n_predictions = cur.execute("SELECT * FROM predictions WHERE matchid=%s",(matchid,))
#     if n_predictions > 0:
#         resp = cur.fetchall()
#         result = []
#         obj = {}
#         for prediction in resp:
#             obj = {
#                 "matchid":prediction[0],
#                 "username":prediction[1],
#                 "prediction":prediction[2]
#             }
#             result.append(obj)
#             obj = {}
#         return jsonify({
#             "msg":"Predictions fetched successfully",
#             "data": result,
#             "number of predictions":n_predictions,
#             "status":200
#         })
#     else:
#         return jsonify({
#             "msg":"No Predictions to fetch",
#             "data": "",
#             "number of predictions":n_predictions,
#             "status":404
#         })

# @app.route('/getpredictions/<string:username>/<string:matchid>',methods=['GET'])
# @jwt_required()
# def getPrediction(username,matchid):
#     cur = mysql.connection.cursor()
#     n_predictions = cur.execute("SELECT * FROM predictions WHERE username=%s AND matchid=%s",(username,matchid))
#     if n_predictions > 0:
#         resp = cur.fetchall()
#         result = []
#         obj = {}
#         for prediction in resp:
#             obj = {
#                 "matchid":prediction[0],
#                 "username":prediction[1],
#                 "prediction":prediction[2]
#             }
#             result.append(obj)
#             obj = {}
#         return jsonify({
#             "msg":"Predictions fetched successfully",
#             "data": result,
#             "number of predictions":n_predictions,
#             "status":200
#         })
#     else:
#         return jsonify({
#             "msg":"No Predictions to fetch",
#             "data": "",
#             "number of predictions":n_predictions,
#             "status":404
#         })

# @app.route('/user/<string:username>',methods=['POST'])
# def u_score(username):
#     req = request.get_json()
#     score = req['score']
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM user WHERE username=%s",(username,))
#     n_user = cur.fetchone()
#     if n_user>0:
#         cur.execute("UPDATE user SET score=%s WHERE username=%s",(score,username))
#         mysql.connection.commit()
#         return jsonify({
#             "msg":"Score updated successfully",
#             "status":200
#         })
#     else:
#         return jsonify({
#             "msg":"Username not found",
#             "status":404
#         })

def calculate_score(match, prediction):
    actual = match['score']['winner']
    predicted = prediction['winner']
    if actual == predicted:
        return 3
    else :
        return 0

@app.route('/updatescore',methods=['GET'])
def update_score():
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': '1aef8588c448420db90524cb64d2455e' }
    connection.request('GET', '/v2/competitions/2021/matches', None, headers )
    apiData = json.loads(connection.getresponse().read().decode())
    apiMatchData = apiData['matches']
    predictions = PerdictionTable.find()
    count = 0
    for prediction in predictions:
        for match in apiMatchData:
            if match['id'] == prediction['matchid'] and match['status'] == "FINISHED":
                score = calculate_score(match, prediction['prediction'])
                prev_score = UserTable.find_one({
                    'username':prediction['username']
                })['score']
                new_score = prev_score + score
                UserTable.find_one_and_update({
                    'username': prediction['username']
                },{"$set":{
                    "score":new_score
                }})
                PerdictionTable.delete_one({
                    'matchid':prediction['matchid'],
                    'username':prediction['username']
                })
                count = count + 1
                break
    return jsonify({
        "msg": "updated score in db",
        "count": count
    })

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_score, trigger="interval", seconds=3600)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
