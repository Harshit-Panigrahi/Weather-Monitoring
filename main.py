from flask import Flask, jsonify, render_template, request
import os, datetime

import firebase_admin
from firebase_admin import credentials, initialize_app, firestore
from key import creds

app = Flask(__name__)

if (not firebase_admin._apps):
  cred = credentials.Certificate(creds)
  default_app = initialize_app(cred)

firebase_db = firestore.client()

@app.route("/add-data", methods=["POST"])
def add_data():
  try:
    temperature = request.json.get("temperature")
    humidity = request.json.get("humidity")
    pressure = request.json.get("pressure")
    altitude = request.json.get("altitude")
    
    doc_ref = firebase_db.collection("Data")
    add_values = doc_ref.document().create(dict(Temperature=temperature, Humidity=humidity, Pressure=pressure, Altitude=altitude, Date=datetime.datetime.utcnow()))
    
    return jsonify({
      "status": "success"
    }), 201
  
  except Exception as e:
    return jsonify({
      "status": "error",
      "message": str(e)
    }), 400

@app.route("/")
def index():
  try:
    doc_ref = firebase_db.collection("Data")
    data = doc_ref.order_by("Date", direction="DESCENDING")
    return render_template("/home/home.html", data=data)
  
  except Exception as e:
    return jsonify({
      "status": "error",
      "message": str(e)
    }), 400
    

if __name__ == '__main__':
  app.run(host='192.168.1.13', port=5000)