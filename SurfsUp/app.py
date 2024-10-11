# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>temperature</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    """Precipitation Analysis"""

    # Query precipitation analysis
    max_date = session.query(func.max(Measurement.date)).scalar()
    max_date_dt = dt.datetime.strptime(max_date, "%Y-%m-%d")
    year_ago = max_date_dt - dt.timedelta(days=365)
    results = session.query(Measurement).filter(Measurement.date >= year_ago).order_by(Measurement.date.desc()).all()

    # Convert list of tuples into normal list
    precipitation_data = {result.date: result.prcp for result in results}

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():

    """Stations Analysis"""

    # Query stations
    stations = session.query(Station.station).all()

    all_stations = list(np.ravel(stations))

    # Return List of stations
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():

    """Temperature Analysis"""

    # Query temperature
    max_date = session.query(func.max(Measurement.date)).scalar()
    max_date_dt = dt.datetime.strptime(max_date, "%Y-%m-%d")
    year_ago = max_date_dt - dt.timedelta(days=365)
    filtered_data = session.query(Measurement).filter(Measurement.date >= year_ago).filter(Measurement.station == 'USC00519281').group_by(Measurement.date).order_by(Measurement.date).all()

    precipitation_data = {row.date: row.tobs for row in filtered_data}

    # Return List of stations
    return jsonify(precipitation_data)

if __name__ == '__main__':
    app.run(debug=True)
