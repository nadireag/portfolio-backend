# import dependencies
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template, request, make_response
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

# create the routes
@app.route('/api/update', methods=['POST'])
def update():
    if request.method == 'POST':
        if request.is_json:

            data = request.get_json()

            name = data['name']
            email = data['email']
            message = data['message']

            new_info  = Info(name=name, email=email, message=message)
            db.session.add(new_info)
            db.session.commit()
            
            return make_response(f'{data} successfully created!')

if __name__ =="__main__":
    app.run(debug=True)
