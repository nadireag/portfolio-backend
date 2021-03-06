# import dependencies
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, json, render_template, request, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
load_dotenv()

# create the flask app
app = Flask(__name__)

# get the heroku database url from environment
db_uri = os.environ['DATABASE_URL']

# app configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# db setup
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(db.engine, reflect=True)

# save references to the table
Info = Base.classes.info

# cors config
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# create the routes
@app.route('/api/update', methods=['POST', 'OPTIONS'])
def update():

    if request.method == 'POST':

        if request.is_json:

            data = request.get_json()

            print(data)
            
            name = data['name']
            email = data['email']
            message = data['message']

            new_info  = Info(name=name, email=email, message=message)
            db.session.add(new_info)
            db.session.commit()
            
            return json.dumps(data), 200, {'ContentType':'application/json'} 
            # return Response(f'{data}', status=200, mimetype='application/json')
            # return make_response(f'{data} successfully created!')

    if request.method == 'OPTIONS':

        return json.dumps({}), 200, {'ContentType':'application/json'} 
        # return Response('{}', status=200, mimetype='application/json')

if __name__ =="__main__":
    app.run(debug=True)
