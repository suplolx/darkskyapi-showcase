from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_app import app, db
from flask_app.forms import LocationForm
from flask_app.translate import days

from DarkSkyAPI.DarkSkyAPI import DarkSkyClient
from flask_app.BingMaps import BingGeoCode
from flask_app.secret import DS_API_KEY, B_API_KEY


@app.route("/", methods=["GET", "POST"])
def index():
    form = LocationForm()
    if form.validate_on_submit() and request.method == "POST":
        location = form.location.data.split(",")
        if len(location) > 1 and len(location) <= 2:
            geocoder = BingGeoCode(B_API_KEY, str(location[0]), country=str(location[1]))
        else:
            geocoder = BingGeoCode(B_API_KEY, str(location[0]))
        client = DarkSkyClient(DS_API_KEY, geocoder.coords, exclude=["minutely"], lang="nl", units="ca")
        context = {
            "current": client.currently,
            "daily": client.daily,
            "hourly": client.hourly,
            "humidity": int(client.currently.humidity * 100),
            "precipProbability": int(client.currently.precipProbability * 100),
            "forecast": zip(
                client.daily.datetimes(date_fmt="%a"), 
                client.daily.icon, 
                client.daily.temperatureHigh, 
                client.daily.temperatureLow, 
                client.daily.precipProbability,
                client.daily.temperatureHighTime,
                client.daily.temperatureLowTime,
                ),
            "location": geocoder.location,
            "district": geocoder.data[0]["address"]["adminDistrict"] if "adminDistrict" in geocoder.data[0]["address"] else None,
            "district_2": geocoder.data[0]["address"]["adminDistrict2"] if "adminDistrict2" in geocoder.data[0]["address"] else None,
        }

        return render_template("index.html", form=form, context=context, days=days)
    return render_template("index.html", form=form)
