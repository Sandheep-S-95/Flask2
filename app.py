from flask import *
import requests
app=Flask(__name__)



@app.route("/",methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/citypage",methods=["GET"])
def citypage():
    return render_template("city.html")

@app.route("/city",methods=["POST"])
def city():
    cityName=request.form["cityName"]
    cityName=cityName.lower()
    try:
        headers = {
            "x-rapidapi-key": "60d952eb8amsh3fb0c42a1c985d1p1fbce5jsn67be98652c4c",
            "x-rapidapi-host": "open-weather13.p.rapidapi.com"
        }
        url = "https://open-weather13.p.rapidapi.com/city/"+cityName+"/EN"

        response = requests.get(url, headers=headers)
        print(response.json())
        response=response.json()
        res={
             "city":response["name"],
             "country":response["sys"]["country"],
             "latitude":response["coord"]["lat"],
             "longitude":response["coord"]["lon"],
             "temp_min":response["main"]["temp_min"],
             "temp_max":response["main"]["temp_max"],
             "temp":response["main"]["temp"]
        }
        return render_template("view_city.html",row=res)
    except Exception as e:
        return render_template("result.html",msg="e "+str(e))

@app.route("/latlongpage",methods=["GET"])
def latlongpage():
    return render_template("latlong.html")

@app.route("/latlong",methods=["POST"])
def latlong():
    lat=request.form["lat"]
    lon=request.form["lon"]
    try:
        url = "https://open-weather13.p.rapidapi.com/city/latlon/"+str(lat)+"/"+str(lon)

        headers = {
            "x-rapidapi-key": "60d952eb8amsh3fb0c42a1c985d1p1fbce5jsn67be98652c4c",
            "x-rapidapi-host": "open-weather13.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        print(response.json())
        response=response.json()
        res={
             "city":response["name"],
             "country":response["sys"]["country"],
             "latitude":response["coord"]["lat"],
             "longitude":response["coord"]["lon"],
             "temp_min":response["main"]["temp_min"],
             "temp_max":response["main"]["temp_max"],
             "temp":response["main"]["temp"]
        }
        return render_template("view_latlong.html",row=res)
    except Exception as e:
        return render_template("result.html",msg="error: "+str("INVALID LATITIUDE LONGITUDE"))
    

@app.route("/aipredictionpage",methods=["GET"])
def aipredictionpage():
    return render_template("aiprediction.html")

@app.route("/aiprediction",methods=["POST"])
def aiprediction():
    lat=request.form["lat"]
    lon=request.form["lon"]
    try:
        url = "https://ai-weather-by-meteosource.p.rapidapi.com/alerts"

        querystring = {"lat":str(lat),"lon":str(lon),"timezone":"auto","language":"en"}

        headers = {
	        "x-rapidapi-key": "60d952eb8amsh3fb0c42a1c985d1p1fbce5jsn67be98652c4c",
	        "x-rapidapi-host": "ai-weather-by-meteosource.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        print(response.json())
        response=response.json()
        eventMsg=""
        severityMsg=""
        print(len(response["alerts"]["data"]))
        if(len(response["alerts"]["data"])==0):
             eventMsg="Safe"
             severityMsg="Safe"
        else:
             eventMsg=response["alerts"]["data"][0]["event"]
             severityMsg=response["alerts"]["data"]["0"]["severity"]
        res={
              "latitude":response["lat"],
              "longitude":response["lon"],
              "event":eventMsg,
              "severity":severityMsg
         }
        return render_template("view_aiprediction.html",row=res)
    except Exception as e:
        return render_template("result.html",msg="error: "+str(e))
    
@app.route("/aistatuspage",methods=["GET"])
def aistatuspage():
    return render_template("aistatus.html")

@app.route("/aistatus",methods=["POST"])
def aistatus():
    lat=request.form["lat"]
    lon=request.form["lon"]
    try:
        url = "https://ai-weather-by-meteosource.p.rapidapi.com/current"

        querystring = {"lat":str(lat),"lon":str(lon),"timezone":"auto","language":"en","units":"auto"}

        headers = {
	        "x-rapidapi-key": "60d952eb8amsh3fb0c42a1c985d1p1fbce5jsn67be98652c4c",
	        "x-rapidapi-host": "ai-weather-by-meteosource.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        print(response.json())
        response=response.json()
        currentMsg=""
        print(len(response["current"]["summary"]))
        if(len(response["current"]["summary"])==0):
             currentMsg="Clear"
        else:
             currentMsg=response["current"]["summary"]
        res={
              "latitude":response["lat"],
              "longitude":response["lon"],
              "status":currentMsg,
         }
        return render_template("view_aistatus.html",row=res)
    except Exception as e:
        return render_template("result.html",msg="error: "+str(e))

@app.route("/forecastpage",methods=["GET"])
def forecastpage():
    return render_template("forecast.html")

@app.route("/forecast",methods=["POST"])
def forecast():
    lat=request.form["lat"]
    lon=request.form["lon"]
    try:
        url = "https://weather-forecast-api3.p.rapidapi.com/weatherForecast"

        querystring = {"latitude":lat,"longitude":lon}

        headers = {
	        "x-rapidapi-key": "60d952eb8amsh3fb0c42a1c985d1p1fbce5jsn67be98652c4c",
	        "x-rapidapi-host": "weather-forecast-api3.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        # print(response.json())

        response=response.json()
        currentMsg=""
        print(response["weatherData"]["hourly"]["temperature_2m"])
        res={
              "current_temp":response["weatherData"]["hourly"]["temperature_2m"][0],
              "next_hour_temp":response["weatherData"]["hourly"]["temperature_2m"][1],
              "after2_hours":response["weatherData"]["hourly"]["temperature_2m"][2]
         }
        return render_template("view_forecast.html",row=res)
    except Exception as e:
        return render_template("result.html",msg="error: "+str(e))

def main():
    app.run(host="0.0.0.0",port=10000,debug=False)
main()
