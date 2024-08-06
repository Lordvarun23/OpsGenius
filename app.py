'''from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Generate dummy data for IT operations
def generate_it_operations_data():
    incidents = []
    for i in range(10):
        incident = {
            "id": i + 1,
            "type": random.choice(["Network Issue", "Server Down", "Software Bug"]),
            "priority": random.choice(["Low", "Medium", "High"]),
            "status": random.choice(["Open", "Resolved", "In Progress"]),
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
        }
        incidents.append(incident)

    performance_metrics = {
        "cpu_usage": random.uniform(0, 100),
        "memory_usage": random.uniform(0, 100),
        "disk_space": random.uniform(0, 100)
    }

    return {"incidents": incidents, "performance_metrics": performance_metrics}

# Generate dummy data for asset management
def generate_asset_management_data():
    assets = []
    for i in range(10):
        asset = {
            "id": i + 1,
            "type": random.choice(["Laptop", "Desktop", "Server", "Router"]),
            "serial_number": f"SN{i+1:05d}",
            "purchase_date": (datetime.now() - timedelta(days=random.randint(0, 1000))).isoformat(),
            "warranty_status": random.choice(["Valid", "Expired"]),
            "location": random.choice(["New York", "San Francisco", "Chicago", "Austin"])
        }
        assets.append(asset)
    return {"assets": assets}

# Generate dummy data for network performance
def generate_network_performance_data():
    network_map = [{"device": f"Device{i}", "status": random.choice(["Online", "Offline"])} for i in range(10)]
    bandwidth_usage = [random.uniform(0, 100) for _ in range(24)]
    latency = [random.uniform(0, 200) for _ in range(24)]
    return {"network_map": network_map, "bandwidth_usage": bandwidth_usage, "latency": latency}

@app.route('/api/it-operations', methods=['GET'])
def get_it_operations():
    return jsonify(generate_it_operations_data())

@app.route('/api/asset-management', methods=['GET'])
def get_asset_management():
    return jsonify(generate_asset_management_data())

@app.route('/api/network-performance', methods=['GET'])
def get_network_performance():
    return jsonify(generate_network_performance_data())

if __name__ == '__main__':
    app.run(debug=False)
'''

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import random
from datetime import datetime, timedelta
import pandas as pd
import joblib
import flask

app = Flask(__name__)
CORS(app)

# Generate dummy data for IT operations
def generate_it_operations_data():
    incidents = []
    for i in range(10):
        incident = {
            "id": i + 1,
            "type": random.choice(["Network Issue", "Server Down", "Software Bug"]),
            "priority": random.choice(["Low", "Medium", "High"]),
            "status": random.choice(["Open", "Resolved", "In Progress"]),
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
        }
        incidents.append(incident)

    performance_metrics = {
        "cpu_usage": random.uniform(0, 100),
        "memory_usage": random.uniform(0, 100),
        "disk_space": random.uniform(0, 100)
    }

    return {"incidents": incidents, "performance_metrics": performance_metrics}

# Generate dummy data for asset management
def generate_asset_management_data():
    assets = []
    for i in range(10):
        asset = {
            "id": i + 1,
            "type": random.choice(["Laptop", "Desktop", "Server", "Router"]),
            "serial_number": f"SN{i+1:05d}",
            "purchase_date": (datetime.now() - timedelta(days=random.randint(0, 1000))).isoformat(),
            "warranty_status": random.choice(["Valid", "Expired"]),
            "location": random.choice(["New York", "San Francisco", "Chicago", "Austin"])
        }
        assets.append(asset)
    return {"assets": assets}

# Generate dummy data for network performance
def generate_network_performance_data():
    network_map = [{"device": f"Device{i}", "status": random.choice(["Online", "Offline"])} for i in range(10)]
    bandwidth_usage = [random.uniform(0, 100) for _ in range(24)]
    latency = [random.uniform(0, 200) for _ in range(24)]
    return {"network_map": network_map, "bandwidth_usage": bandwidth_usage, "latency": latency}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/api/it-operations', methods=['GET'])
def get_it_operations():
    return jsonify(generate_it_operations_data())

@app.route('/api/asset-management', methods=['GET'])
def get_asset_management():
    return jsonify(generate_asset_management_data())

@app.route('/api/network-performance', methods=['GET'])
def get_network_performance():
    return jsonify(generate_network_performance_data())

@app.route('/api/generate-html', methods=['GET'])
def generate_html():
    # Generate HTML content for the dashboard report
    html_content = "<h1>Dashboard Report</h1>"
    html_file = "/path/to/dashboard_report.html"
    with open(html_file, "w") as file:
        file.write(html_content)
    return send_file(html_file, download_name="dashboard_report.html", as_attachment=True)


@app.route('/view-csv')
def view_csv():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('anomaly_detect.csv')

    # Convert the DataFrame to HTML table
    table_html = df.to_html(classes='table table-striped', index=False)

    # Render the HTML table in a new template
    return render_template('view_csv.html', table_html=table_html)

@app.route('/api/chatbot', methods=['POST'])
def handle_chatbot_message():
    user_message = request.json.get('message')
    # Simulate a response from the chatbot
    bot_response = f"You said: {user_message}"
    return jsonify({"response": bot_response})

@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/api/predict', methods=['POST'])
def predict_result():
    # Get the input from the request
    model = joblib.load('ticket_classifier_model.pkl')
    user_input = request.json.get('input')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Perform prediction
    prediction = model.predict([user_input])[0]

    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=False)

