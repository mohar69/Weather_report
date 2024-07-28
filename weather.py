from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    weather = None
    return render_template('weather.html', weather=weather)

@app.route('/weather', methods=['POST'])
def get_weather():
    pic_icons = [
        "/static/images/sunny.jpeg",
        "/static/images/rain.jpeg",
        "/static/images/cloud.jpeg",
        "/static/images/snowy.jpeg",
        "/static/images/fog.jpeg",
        "/static/images/cloud-sun.jpeg",
        "/static/images/thunder.jpeg",
    ]

    icons = [
        "/static/icons/animated/not_available.jpeg", "/static/icons/animated/not_available.jpeg",
        "/static/icons/animated/day.svg", "/static/icons/animated/cloudy-day-1.svg",
        "/static/icons/animated/cloudy-day-2.svg", "/static/icons/animated/cloudy-day-3.svg",
        "/static/icons/animated/cloudy.svg", "/static/icons/animated/cloudy.svg",
        "/static/icons/animated/cloudy-day-3.svg", "/static/icons/animated/fog.jpeg",
        "/static/icons/animated/rainy-4.svg", "/static/icons/animated/rainy-5.svg",
        "/static/icons/animated/rainy-1.svg", "/static/icons/animated/rainy-6.svg",
        "/static/icons/animated/thunder.svg", "/static/icons/animated/thunder.svg",
        "/static/icons/animated/snowy-2.svg", "/static/icons/animated/snowy-4.svg",
        "/static/icons/animated/snowy-1.svg", "/static/icons/animated/snowy-6.svg",
        "/static/icons/animated/rainy-7.svg", "/static/icons/animated/rainy-7.svg",
        "/static/icons/animated/rainy-7.svg", "/static/icons/animated/weather.svg",
        "/static/icons/animated/weather.svg", "/static/icons/animated/rainy-7.svg",
        "/static/icons/animated/day.svg", "/static/icons/animated/cloudy-day-1.svg",
        "/static/icons/animated/cloudy-day-2.svg", "/static/icons/animated/cloudy-day-3.svg",
        "/static/icons/animated/cloudy.svg", "/static/icons/animated/rainy-1.svg",
        "/static/icons/animated/rainy-6.svg", "/static/icons/animated/thunder.svg",
        "/static/icons/animated/snowy-6.svg", "/static/icons/animated/weather.svg",
        "/static/icons/animated/weather.svg"
    ]

    arr = [
        "not_available", "not_available", "sunny", "mostly_sunny", "partly_sunny", "mostly_cloudy",
        "cloudy", "overcast", "overcast_with_low_clouds", "fog", "light_rain", "rain", "possible_rain",
        "rain_shower", "thunderstorm", "local_thunderstorms", "light_snow", "snow", "possible_snow",
        "snow_shower", "rain_and_snow", "possible_rain_and_snow", "rain_and_snow", "freezing_rain",
        "possible_freezing_rain", "hail", "clear_night", "mostly_clear_night", "partly_clear_night",
        "mostly_cloudy_night", "cloudy_night", "overcast_with_low_clouds_night", "rain_shower_night",
        "local_thunderstorms_night", "snow_shower_night", "rain_and_snow_night", "possible_freezing_rain_night"
    ]

    map = {arr[i]: icons[i] for i in range(len(arr))}

    place = request.form['place']

    url = "https://ai-weather-by-meteosource.p.rapidapi.com/find_places"
    querystring = {"text": place, "language": "en"}
    headers = {
        "X-RapidAPI-Key": "012dc27df3msh97afb7adef8fe23p1721dejsn340b821c5230",
        "X-RapidAPI-Host": "ai-weather-by-meteosource.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        place_data = response.json()[0]
        latitude = place_data['lat']
        longitude = place_data['lon']
        placename = place_data['name']
    else:
        return render_template('error.html', error='No data found for the specified place')

    url = "https://ai-weather-by-meteosource.p.rapidapi.com/current"
    querystring = {
        "lat": latitude,
        "lon": longitude,
        "timezone": "auto",
        "language": "en",
        "units": "auto"
    }


    lat=float(latitude[:-1:])
    lon=float(longitude[:-1:])

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        weather_data = response.json()
        icon_num = weather_data["current"]["icon_num"]

        sunny = [2, 3, 26, 27]
        rain = [10, 11, 12, 13, 25, 32, 23, 24, 36]
        cloudy = [6, 7, 8, 30, 31]
        snowy = [16, 17, 18, 19, 20, 21, 22, 35, 34]
        fog = [9, 1, 0]
        thunder = [14, 15, 33]
        cloudy_sunny = [28, 4, 5, 29]

        if icon_num in sunny:
            pic_url = pic_icons[0]
        elif icon_num in rain:
            pic_url = pic_icons[1]
        elif icon_num in cloudy:
            pic_url = pic_icons[2]
        elif icon_num in snowy:
            pic_url = pic_icons[3]
        elif icon_num in fog:
            pic_url = pic_icons[4]
        elif icon_num in cloudy_sunny:
            pic_url = pic_icons[5]
        elif icon_num in thunder:
            pic_url = pic_icons[6]



        # Starting of GET_DAILY request
        url = "https://ai-weather-by-meteosource.p.rapidapi.com/daily"
        querystring = {"lat": latitude, "lon": longitude, "language": "en", "units": "auto"}
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            prediction_data = response.json()
            temp_data = prediction_data["daily"]["data"][0]['weather'].split("_")
            predictedWeather=" ".join(temp_data).capitalize()

            url = "https://ai-weather-by-meteosource.p.rapidapi.com/hourly"

            querystring = {"lat":latitude,"lon":longitude,"timezone":"auto","language":"en","units":"auto"} 
            response = requests.get(url, headers=headers, params=querystring)

            if response.status_code == 200:
                hour_data = response.json()
                print(hour_data["hourly"]["data"][0]["date"][11::]," : ", hour_data["hourly"]["data"][0]["temperature"])

                jsonData = {
                "x": [],
                "y": []
                }

                for i in range(12):
                    num=int(hour_data["hourly"]["data"][i]["date"][11:13:])
                    if num ==24:
                        data="00 AM"
                    elif num ==12:
                        data="12 PM"
                    elif num >12:
                        data=str(num-12)+ " PM"
                    else:
                        data=str(num)+ " AM"


                    jsonData["x"].append(data)
                    jsonData["y"].append(hour_data["hourly"]["data"][i]["temperature"])

                    src = [""] * 8
                    for i in range(8):
                        if prediction_data["daily"]["data"][i]['weather'] in arr:
                            src[i] = map[prediction_data["daily"]["data"][i]['weather']]
                        else:
                            if "rain" in prediction_data["daily"]["data"][i]['weather'] :
                                src[i] = "/static/icons/animated/rainy-7.svg"
                            elif "snow" in prediction_data["daily"]["data"][i]['weather']:
                                src[i] = "/static/icons/animated/snowy-4.svg"
                            elif "sun" in prediction_data["daily"]["data"][i]['weather']:
                                src[i] = "/static/icons/animated/weather.svg"
                            elif "cloud" in prediction_data["daily"]["data"][i]['weather']:
                                src[i] = "/static/icons/animated/cloudy-day-2.svg"
                            elif "thunder" in prediction_data["daily"]["data"][i]['weather'] or "storm" in prediction_data["daily"]["data"][i]['weather']:
                                src[i] = "/static/icons/animated/thunder.svg"
                            else:
                                src[i] = "/static/icons/animated/not_available.jpeg"

                return render_template('weather.html', latitude=lat, longitude=lon, weather=weather_data, prediction=prediction_data, icon=icons, pic_urls=pic_url, place=placename, map=map,predictedWeather=predictedWeather, jsonData=jsonData, arr = arr, src = src)
            else:
                return render_template('error.html', error='Failed to fetch weather data'), response.status_code
        else:
            return render_template('error.html', error='Failed to fetch weather data'), response.status_code
    else:
        return render_template('error.html', error='Failed to fetch weather data'), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

