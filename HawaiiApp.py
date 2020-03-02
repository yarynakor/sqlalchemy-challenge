#!/usr/bin/env python
# coding: utf-8


import numpy as np
import datetime as dt 
import pandas as pd 


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)



# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/temperature<br/>"      
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation(date):
    """Return a dictionary of precipitation information"""
    # session = Session(engine)
    rainfall = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()
    prdict = {date: x for date, x in rainfall}
    return jsonify(prdict)


@app.route("/api/v1.0/stations")
def station():
    # Query all stations
    results = session.query(Station.station).all()
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)


@app.route("/api/v1.0/temperature")
def tobs():
    temps = session.query(Measurement.tobs).filter(Measurement.date >= '2017,8,23').all()
    tobs_list = list(np.ravel(temps))
    return jsonify (tobs_list)

@app.route ("/api/v1.0/<start>/<end>")
def temps(start,end):
    findings = session.query(Measurement).filter(Measurement.date>= start).filter(Measurement.date<=end)
    found =[] 
    for row in findings:
        found.append(row.tobs) 
    return (jsonify ({"tempmin": min(found),"tempmax": max(found),"tempavg":np.mean}))
           
    session.close()


if __name__ == '__main__':
    app.run(debug=True)

