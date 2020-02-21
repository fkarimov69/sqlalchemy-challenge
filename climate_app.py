import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.hybrid import hybrid_property

from flask import Flask, jsonify
from datetime import datetime


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#Base.classes.keys()
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session=Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# # 

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """Available routes"""
    return(
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/stations:<br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    session=Session(engine)
    results=session.query(Measurement.prcp).all()
    session.close()

    all_prcp=list(np.ravel(results))
    return jsonify(all_prcp)

@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    results=session.query(Measurement.date,Measurement.station,Measurement.tobs).order_by((Measurement.date).desc()).first()
    session.close()

    all_tobs=list(np.ravel(results))
    return jsonify(all_tobs)

@app.route("/api/v1.0/stations")
def station():
    session=Session(engine)
    results=session.query(Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    session.close()

    all_station=[]
    for station,name,latitude,longitude,elevation in results:
        station_dict={}
        station_dict["station"]=station
        station_dict["name"]=name
        station_dict["latitude"]=latitude
        station_dict["longitude"]=longitude
        station_dict["elevation"]=elevation
        all_station.append(station_dict)
    
    return jsonify(all_station)

@app.route("/api/v1.0/range/<start>/<end>")
def tobs_range(start,end):
    
    session=Session(engine)
    results=session.query(func.min(Measurement.tobs),
    func.avg(Measurement.tobs),
    func.max(Measurement.tobs).\
        filter(Measurement.date>=start,Measurement.date<=end)).first()
    session.close()
    
    return str(results)

# @property
# def calculated_date(self):
#     return date(self.year, self.month, self.day)

@app.route("/api/v1.0/date/<start>")
def tobs_date(start):
# @property
# def calculated_date(self):
#     return Measurement.date(self.year, self.month, self.day)

    session=Session(engine)
    print(start)
    results=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs).\
        filter(Measurement.date>start)).all()
    session.close()
    
    return str(results)

if __name__=='__main__':
    app.run(debug=True)


