import mars_data as md
import datetime as dt
import numpy as np
import pandas as pd
import pymongo
import pprint

# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine, func

from flask import Flask, render_template, jsonify, redirect
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

#################################################
# Application Setup
#################################################

#################################################
# Calculate Start and End date for past 1 year
#################################################

# end_dt = datetime.today().strftime('%Y-%m-%d')
# start_dt = (datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d')

#################################################
# Database Setup
#################################################
# connection_str = 'sqlite:///hawaii.sqlite'
# engine = create_engine(connection_str)

# reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(engine, reflect=True)

# Save reference to the table
# Measurement = Base.classes.measurement
# Station = Base.classes.station

# Create our session (link) from Python to the DB
# session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# results = []

#Default Route#
@app.route("/")
def welcome():
    # res1 = md.scrape()
    # return jsonify(res1)
    conn = "mongodb://test:test@ds243335.mlab.com:43335/heroku_smxwwn9d"
    client = pymongo.MongoClient(conn)

    db = client.heroku_smxwwn9d
    # data1 = db.mars_collection.find()
    mars_collection = db.mars_collection

    for post1 in db.mars_collection.find().sort('time', 1):
        print(post1)
        print("################")

    title_list, url_list = [], []
    # results = []
    for k,v in post1.items():
        print(k)
        print(v)
        print("----------")
        if(k == '_id'):
            pass
        else:
            if(k == 'df_mars'):
                # results.append(v)
                results = pd.read_json(v).to_html()
            if(k == 'hemisphere_image_urls'):
                for x in v:
                    print(x)
                    title_list.append(x['title'])
                    url_list.append(x['img_url'])
                    print("---")
                # print(v)

    # return jsonify(results)
    return render_template("index.html", results=post1, results2=results, results3=title_list, results4=url_list)


#Default Route#
@app.route("/scrape")
def scrape1():
    conn = "mongodb://test:test@ds243335.mlab.com:43335/heroku_smxwwn9d"
    client = pymongo.MongoClient(conn)

    db = client.heroku_smxwwn9d
    # data1 = db.mars_collection.find()
    mars_collection = db.mars_collection

    res1 = md.scrape()
    mars_collection.insert_one(res1)

    # for post1 in db.mars_collection.find():
    #     print(post1)

    # results = []
    # for k,v in post1.items():
    #     print(k)
    #     print(v)
    #     print("----------")
    #     if(k == '_id'):
    #         pass
    #     else:
    #         results.append({k:v})

    return redirect("http://localhost:5000/", code=302)

    # return "Successfully collected data."


#Route for precipitation data during past year#
# @app.route("/api/v1.0/precipitation")
# def Precipitation():
#     dict_1 = {}
#     results = session.query(Measurement.date.label('date'), Measurement.prcp.label('prcp')).filter(Measurement.date.between(start_dt, end_dt))

#     for result in results:
#         dict_1[result.date.strftime('%Y-%m-%d')] = float(result.prcp)

#     return jsonify(dict_1)

# #Route for stations list#
# @app.route("/api/v1.0/stations")
# def Stations():
#     stations = []
#     results = session.query(Station.name).all()

#     for result in results:
#         stations.append(result)

#     return jsonify(stations)

# #Route for temperature observations data#
# @app.route("/api/v1.0/tobs")
# def TempObservations():
#     temObs = []
#     results = session.query(Measurement.tobs).all()

#     for result in results:
#         temObs.append(float(result.tobs))

#     return jsonify(temObs)

# #Route for temperature observations since a start date#
# @app.route("/api/v1.0/<start>")
# def TempStats(start):
#     dict_2 = {}
#     results = session.query(func.max(Measurement.tobs).label('max_temp'), func.min(Measurement.tobs).label('min_temp'), func.avg(Measurement.tobs).label('avg_temp')).filter(Measurement.date >= start).all()

#     for result in results:
#         dict_2['max_temp'] = float(result.max_temp)
#         dict_2['min_temp'] = float(result.min_temp)
#         dict_2['avg_temp'] = float(result.avg_temp)

#     return jsonify(dict_2)

# #Route for temperature observations between a start and end date#
# @app.route("/api/v1.0/<start>/<end>")
# def TempStats1(start, end):
#     dict_3 = {}
#     results = session.query(func.max(Measurement.tobs).label('max_temp'), func.min(Measurement.tobs).label('min_temp'), func.avg(Measurement.tobs).label('avg_temp')).filter(Measurement.date.between(start, end)).all()

#     for result in results:
#         dict_3['max_temp'] = float(result.max_temp)
#         dict_3['min_temp'] = float(result.min_temp)
#         dict_3['avg_temp'] = float(result.avg_temp)

#     return jsonify(dict_3)


if __name__ == '__main__':
    app.run(debug=True)
