import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define a mock danger zone (bounding box coordinates)
# You can adjust these latitude and longitude boundaries as needed
DANGER_ZONE = {
    "min_lat": 28.6000,
    "max_lat": 28.7000,
    "min_lng": 77.4000,
    "max_lng": 77.5000
}

@app.route('/check', methods=['POST'])
def check_safety():
    # Receive JSON data sent from MIT App Inventor (Web1.PostText)
    data = request.get_json()
    
    if not data or 'latitude' not in data or 'longitude' not in data:
        return jsonify({"error": "Invalid data format"}), 400
    
    try:
        lat = float(data['latitude'])
        lng = float(data['longitude'])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid numerical coordinates"}), 400
    
    # Check if coordinates fall inside the danger zone box
    is_in_danger = (
        DANGER_ZONE["min_lat"] <= lat <= DANGER_ZONE["max_lat"] and
        DANGER_ZONE["min_lng"] <= lng <= DANGER_ZONE["max_lng"]
    )
    
    if is_in_danger:
        return jsonify({
            "status": "danger",
            "message": "High-risk zone detected! Sending safety alerts..."
        })
    else:
        return jsonify({
            "status": "safe",
            "message": "Area is secure."
        })

if __name__ == '__main__':
    # Render assigns dynamic ports via the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
