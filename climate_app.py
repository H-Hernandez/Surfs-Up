# Import dependencies  
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Connection

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# Create a flask for climate_app
climate_app = Flask(__name__)

#Create the routes
@climate_app.route("/")
def home():
    return(f"Available routes<br>"
           f"route: /api/v1.0/precipitation , def: Precipitation data<br>"
           f"route: /api/v1.0/stations , def: List of Stations<br>"
           f"route: /api/v1.0/tobs , def: Date and temp observations from a year from the last data point<br>"
           f"route: /api/v1.0/startdate , def: When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date<br>"
           f"route: /api/v1.0/startdate/enddate , def: Minimum temperature, the average temperature, and the max temperature for a given start or start-end range. Or, When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.")

@climate_app.route("/api/v1.0/precipitation")
def precipitation():

    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').all()

    precipitation_data_dic = dict(precipitation_data)

    return jsonify(precipitation_data_dic)

if __name__ == "__main__":
    climate_app.run(debug=True)

