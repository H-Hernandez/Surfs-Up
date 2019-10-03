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
           f"route: /api/v1.0/precipitation<br>"
           f"route: /api/v1.0/stations<br>"
           f"route: /api/v1.0/tobs<br>"
           f"route: /api/v1.0/2016-07-31<br>"
           f"route: /api/v1.0/2011-01-01/2011-12-31")

@climate_app.route("/api/v1.0/precipitation")
def precipitation():

    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').all()

    precipitation_data_dict = dict(precipitation_data)

    return jsonify(precipitation_data_dict)

@climate_app.route("/api/v1.0/stations")
def stations():

    stations = session.query(Station.name).all()
    station_list = list(np.ravel(stations))

    return jsonify(station_list)

@climate_app.route("/api/v1.0/tobs")
def temp_observ():

    temps_observ = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23')

    temps_observ_list = list(temps_observ)

    return jsonify(temps_observ_list)

@climate_app.route("/api/v1.0/<start>")
def start(start):

    from_start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    from_start_list=list(from_start)
    
    return jsonify(from_start_list)

@climate_app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    between_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    between_dates_list=list(between_dates)

    return jsonify(between_dates_list)

if __name__ == "__main__":
    climate_app.run(debug=True)

