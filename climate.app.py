import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
from flask import Flask, jsonify, request

#################
# Database Setup
#################

engine = create_engine(r'sqlite:///C:\Users\Claudia\Documents\USC-Bootcamp\sqlalchemy-challenge\Resources\hawaii.sqlite')
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement

# Save references to each table
Station = Base.classes.station

#Create Session
Session = Session(engine)

###########
#Setup Flask
###########

#Flask App
app = Flask(__name__)

#######
#Routes
#######
@app.route("/")
def welcome():
    "List all api routes"

    return(
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"List of last 12 month rain totals from stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"List of Station numbers and names<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"List of prior year temperatures from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f" When the start date is (YYYY-MM-DD), calculate the MIN/AVG/MAX temperatures from all dates greater or equal to from the start stations<br/>"
        f"/api/v1.0/start/end<br/>"
        f" Calculate the MIN/AVG/MAX temperatures for all the dates between the start and end date<br/>"
    )
    

@app.route("/api/v1.0/precipitation")
def precip():

    print("Recieved request for Precipitation")
    tobs_all = []
    results = Session.query(Measurement).filter(Measurement.date > '2016-08-24').filter(Measurement.date <= '2017-08-23').all()
    for data in results:
        tobs_dict = {}
        print(vars(data))
        tobs_dict[data.date] = data.prcp
        tobs_all.append(tobs_dict)
        
    return jsonify(tobs_all)


@app.route("/api/v1.0/stations/")
def stations():    
    
    print("Recieved request for Sations")
    #"Return a JSON list of sations from the dataset."

    #Query stations
    station_results = Session.query(Station.station).all()
    
    #Convert tuples into normal list
    station_list = list(np.ravel(station_results))
    
    return jsonify(station_list)


@app.route("/api/v1.0/tobs/")
def tobs():
    print("Recieved request for tobs")
    #"Return a JSON list of Temperature Observations (TOBS) for the previous year"
    
    #Query tobs
    tobs_results = Session.query(Measurement.tobs).all()
    
    #Convert tuples into normal list
    tobs_list = list(np.ravel(tobs_results))
    
    return jsonify(tobs_list)


@app.route("/api/v1.0/start/")
def tobs_start():
    startdate = request.args.get('startdate')    

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
    return jsonify(Session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).all())

@app.route("/api/v1.0/start/end")
def tobs_date_range():
    startdate = request.args.get('startdate')
    enddate = request.args.get('enddate')

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
    return jsonify(Session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all())
    
    
if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    