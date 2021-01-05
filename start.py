from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123@localhost/test_fil_bill'

db = SQLAlchemy(app)


class HotWaterEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, date, value):
        self.date = date
        self.value = value


class ColdWaterEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, date, value):
        self.date = date
        self.value = value


db.create_all()


@app.route('/', methods=["GET"])
def index():
    hot_max_value = db.session.query(func.max(HotWaterEntry.value).label("max_value")).one()
    cold_max_value = db.session.query(func.max(ColdWaterEntry.value).label("max_value")).one()
    return render_template("index.html", hot_max_value=hot_max_value[0], cold_max_value=cold_max_value[0])


@app.route('/hot-water', methods=["GET"])
def get_hot_water_page():
    max_value = db.session.query(func.max(HotWaterEntry.value).label("max_value")).one()
    hot_water_entries = HotWaterEntry.query.all()
    hot_water_entries.reverse()
    return render_template("hotWater.html", hot_water_values=hot_water_entries, max_value=max_value.max_value)


@app.route('/hot-water/add', methods=["POST"])
def add_hot_water_value():
    value = request.form['value']
    HotWaterEntry.query.all()
    db.session.add(HotWaterEntry(datetime.now(), value))
    db.session.commit()
    return redirect(url_for("get_hot_water_page"))


@app.route('/cold-water', methods=["GET"])
def get_cold_water_page():
    max_value = db.session.query(func.max(ColdWaterEntry.value).label("max_value")).one()
    return render_template("coldWater.html", cold_water_values=ColdWaterEntry.query.all(),
                           max_value=max_value[0])


@app.route('/cold-water/add', methods=["POST"])
def add_cold_water_value():
    value = request.form['value']
    ColdWaterEntry.query.all()
    db.session.add(ColdWaterEntry(datetime.now(), value))
    db.session.commit()
    return redirect(url_for("get_cold_water_page"))
