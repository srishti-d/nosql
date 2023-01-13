from bson.objectid import ObjectId
from flask import Flask, json, render_template
import requests
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask import jsonify, request
from werkzeug.utils import redirect
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib


app = Flask(__name__)
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/medcharge")
db = mongodb_client.db

app.config['MONGO_URI'] = "mongodb://localhost:27017/medcharge"
mongodb_client = PyMongo(app)
db = mongodb_client.db


@app.route('/records')
def records():
    records = db.records.find()
    resp = dumps(records)
    return resp

@app.route('/records/<id>')
def record(id):
    records = db.records.find_one({'_id': ObjectId(id)})
    resp = dumps(records)
    return resp

@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete_record(id):
    db.records.delete_one({'_id': ObjectId(id)})
    resp = jsonify("Record deleted successfully")
    resp.status_code = 200
    return redirect('/')
    return resp

@app.route('/update/<id>', methods=['POST', 'GET'])
def update_record(id):
    if request.method == 'POST':
        _id = id
        _age = int(request.form['Age'])
        _gender = request.form['Gender']
        _bmi = float(request.form['BMI'])
        _children = int(request.form['Children'])
        _smoker = request.form['Smoker']
        _charges = float(request.form['Charges'])
        id = db.records.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id
    else ObjectId(_id)}, {'$set': {'Age': _age, 'Gender': _gender, 'BMI': _bmi, 'Children': _children,'Smoker': _smoker, 'Charges': _charges}})
        resp = jsonify("Record updated successfully")

    resp.status_code = 200
    return redirect('/')
    return resp

# Frontend
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        req = requests.get('http://127.0.0.1:80/records')
        data = json.loads(req.content)
        return render_template('index.html', data=data)
    elif request.method == 'POST':
        _age = int(request.form['Age'])
        _gender = request.form['Gender']
        _bmi = float(request.form['BMI'])
        _children = int(request.form['Children'])
        _smoker = request.form['Smoker']
        _charges = float(request.form['Charges'])

        id =  db.records.insert_one({'Age': _age, 'Gender': _gender, 'BMI': _bmi,
        'Children': _children, 'Smoker': _smoker, 'Charges': _charges})
    resp = jsonify("Record added successfully")
    resp.status_code = 200
    return redirect('/')

@app.route('/xyz', methods=['GET'])
def stats():
    if request.method == 'GET':
        req = requests.get('http://127.0.0.1:80/records')
        cursor = db.records.find().limit(1000)
        df = pd.DataFrame(list(cursor))
        df["Charges"] = df.Charges.astype(str).astype(float)
        df["Smoker"] = df.Smoker.astype(str).astype(str)
        df["Age"] = df.Age.astype(str).astype(int)
        print(df)
    
    #Generating Plot 1
        # plt.subplot(1,2,1)
    
        plt.bar(df["Age"],df["Charges"])
        plt.xlabel("Age")
        plt.ylabel("Charges")
        plt.show()
        # plt.savefig('Backend/static/plot1.png')
    
     #Generating Plot 2
        # plt.subplot(1,2,2)
        plt.scatter(df["Age"],df["BMI"])
        plt.xlabel("Age")
        plt.ylabel("BMI")
        plt.show()
        # plt.savefig('Backend/static/plot2.png')
    return redirect('/')

# @app.route('/')
# def dashboard():
#     records = db.records.find()
#     resp = dumps(records)
#     # total_users = 0
#     # recent24h_users = 0
#     # recentWeek_users = 0
#     age_20 = 0
#     agelt_20 = 0
#     for item in resp:
#         total_users = total_users + 1
#         if item['Age'] > 20:      
#             age_20 = age_20 + 1
#         if item['Age'] < 20:
#             agelt_20 = agelt_20 
#         # if item['created_at'] > (datetime.now() - timedelta(hours=168)): 
#         #     recentWeek_users = recentWeek_users + 1
    
#     getKPIUsers = {
#             'Age': age_20,
#             'AgeLt': agelt_20
            
#     }
#     return render_template('dashboard.html', KPIUsers=getKPIUsers)
    
    

#End Frontend

@app.errorhandler(404)
def not_found(error = None):
    message = {
    'status' : 404,
    'message' : 'Not Found '+ request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run(port=80, debug=True)

