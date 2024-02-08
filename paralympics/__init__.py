import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import csv
from pathlib import Path

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def add_data_from_csv():

    from paralympics.model import Region, Event

    #if there is not regions in the database, then add them 
    first_region = db.session.execute(db.select(Region)).first()
    if not first_region:
        print("Start adding region data to the database")
        noc_file = Path(__file__).parent.parent.joinpath('data', 'noc_regions.csv')
        with open(noc_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                r = Region(NOC=row[0], region=row[1], notes=row[2])
                db.session.add(r)
            db.session.commit()

    #if there is not events in the database, then add them
    first_event = db.session.execute(db.select(Event)).first()
    if not first_event:
        print("Start adding event data to the database")
        event_file = Path(__file__).parent.parent.joinpath('data', 'paralympic_events.csv')
        with open(event_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                e = Event(type=row[0],
                          year=row[1],
                            country=row[2],
                            host=row[3],
                            NOC=row[4],
                            start=row[5],
                            end=row[6],
                            duration=row[7],
                            disabilities_included=row[8],
                            countries=row[9],
                            events=row[10],
                            sports=row[11],
                            participants_m=row[12],
                            participants_f=row[13],
                            participants=row[14],
                            highlights=row[15])
                db.session.add(e)
            db.session.commit()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #configure the app to use the database
    app.config.from_mapping(
        SECRET_KEY='bd4wZvHjEx3u_Rfb6gyxmA',
        #set the path of the database
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'paralympics.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #initialize FLask with the SQLAlchemy database extension
    db.init_app(app)

    from paralympics.model import Region, Event, User

    with app.app_context():
    # register the routes with the app in the context
        db.create_all()
        add_data_from_csv()
        from paralympics import route


    return app


    
   