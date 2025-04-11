from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get MongoDB URI from environment variable
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["restaurant_automation"]
bookings = db["bookings"]

@app.route('/update-booking-status', methods=['PATCH'])
def update_booking_status():
    data = request.get_json()
    booking_id = data.get("booking_id")
    status = data.get("status")

    if not booking_id or not status:
        return jsonify({"error": "booking_id and status required"}), 400

    result = bookings.update_one(
        {"booking_id": booking_id},
        {"$set": {"status": status}}
    )

    if result.matched_count == 0:
        return jsonify({"message": "Booking not found"}), 404

    return jsonify({"message": "Booking status updated successfully"}), 200

# Add a simple health check endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "API is running"}), 200

# This is for local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)
