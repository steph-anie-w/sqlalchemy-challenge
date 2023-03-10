# Import Dependencies
import sqlalchemy
import datetime as data
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Establish connection to SQLite file
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Reflect
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references within database
measurement = Base.classes.measurement
station = Base.classes.station

# Initialize flask
app = Flask(__name__)

# Define routes
@app.route("/")
def homepage():
    print(f'Welcome to my API<br/>')
    return(
        f'Available routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'
    )

# Create route for precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    most_recent_date = session.query(measurement.date).\
        order_by(measurement.date.desc()).first()
    most_recent_dt = dt.datetime.strptime(most_recent_date, "%Y-%m-%d").date()
    yr_prior_date = most_recent_dt - dt.timedelta(days= 365)
    yr_prior_dt = dt.datetime.strptime(yr_prior_date, "%Y-%m-%d").date()

    prcp_results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date.between(yr_prior_dt, most_recent_dt)).all()
    
    session.close()

    precipitation = []

    for date, prcp in prcp_results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation.append(precipitation_dict)
    return jsonify(precipitation)

# Create route for stations
@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    station_query = session.query(station.station, station.id).all()
    
    session.close()

    station_info = []

    for station, id in station_query:
        station_dict = {}
        station_dict['station'] = station
        station_dict['id'] = id
        station_info.append(station_dict)
    return jsonify(station_info)

# Create route for temperature
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    active_station = session.query(measurement.station, func.count(measurement.station)).\
        order_by(func.count(measurement.station).desc()).\
        group_by(measurement.station).first()
    most_active = active_station[0]

    tobs_info = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= yr_prior_dt).\
        filter(measurement.station == most_active)
    
    session.close()

    tobs_list = []

    for date, tobs in tobs_info:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

# Create route using start date
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    session.close()

# Create route using start and end date
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)

    session.close()

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

if __name__ == "__main__":
    app.run(debug=False)