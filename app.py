from flask import Flask, jsonify, request
from weather import get_location_coords, get_weather
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/api/weather", methods=["GET"])
def get_weather_data():
    location_name = request.args.get("location")
    
    if not location_name:
        return jsonify({"error": "Location parameter is required"}), 400
    
    location_data = get_location_coords(location_name)
    
    if not location_data:
        return jsonify({"error": "Invalid location. Please try again."}), 404
    
    weather_data = get_weather(location_data["latitude"], location_data["longitude"])
    
    return jsonify({
        "location": {
            "city": location_data["city"],
            "country": location_data["country"],
            "coordinates": {
                "latitude": location_data["latitude"],
                "longitude": location_data["longitude"]
            }
        },
        "weather": [
            {
                "temperature": temp,
                "humidity": humidity,
                "time": time
            } for temp, humidity, time in weather_data
        ]
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)