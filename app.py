from flask import Flask, jsonify

app = Flask(__name__)

slots = ["A1", "A2", "A3"]

@app.route("/")
def home():
    return "Smart Parking System Running"

@app.route("/slots")
def get_slots():
    return jsonify(slots)

if __name__ == "__main__":
    app.run(debug=True)