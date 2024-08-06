import pyshark
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import threading
import time
import warnings
warnings.filterwarnings("ignore")
import csv

# Global variables
features = []
model = None
scaler = StandardScaler()

# Function to process packets and extract features
def process_packet(packet, features):
    try:
        packet_info = {
            'timestamp': packet.sniff_time.timestamp(),
            'src_ip': packet.ip.src,
            'dst_ip': packet.ip.dst,
            'src_port': int(packet[packet.transport_layer].srcport),
            'dst_port': int(packet[packet.transport_layer].dstport),
            'protocol': packet.transport_layer,
            'length': int(packet.length),
            'inter_arrival_time': 0  # Placeholder for inter-arrival time
        }
        if features:
            last_packet_time = features[-1]['timestamp']
            packet_info['inter_arrival_time'] = packet_info['timestamp'] - last_packet_time
        features.append(packet_info)
    except AttributeError:
        pass

# Capture network traffic
interface = 'Wi-Fi'
capture = pyshark.LiveCapture(interface=interface)

# Preprocess and update features
def preprocess_features(features):
    df = pd.DataFrame(features)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['protocol'] = df['protocol'].astype('category').cat.codes
    df['inter_arrival_time'] = df['inter_arrival_time'].fillna(0)

    # Normalize the data
    feature_columns = ['src_port', 'dst_port', 'protocol', 'length', 'inter_arrival_time']
    df[feature_columns] = scaler.fit_transform(df[feature_columns])
    return df

# Train initial model
def train_model(features):
    df = preprocess_features(features)
    feature_columns = ['src_port', 'dst_port', 'protocol', 'length', 'inter_arrival_time']
    model = IsolationForest(contamination=0.01)
    model.fit(df[feature_columns])
    return model

# Update model with new data periodically
def update_model():
    global model, features
    while True:
        time.sleep(36)  # Update model every hour
        if features:
            model = train_model(features)

# Real-time anomaly detection
def real_time_detection(packet):
    global model
    new_features = []
    process_packet(packet, new_features)
    if new_features:
        new_data = preprocess_features(new_features).iloc[-1]
        feature_columns = ['src_port', 'dst_port', 'protocol', 'length', 'inter_arrival_time']
        anomaly = model.predict([new_data[feature_columns]])[0]
        # Specify the filename
        filename = 'anomaly_detect.csv'
        print(list(new_features[-1].values())+ [anomaly])
        # Write data to CSV
        with open(filename, 'a', newline='') as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)
            # Write the rows

            writer.writerows([list(new_features[-1].values())+ [anomaly]])
        if anomaly == -1:
            print(f"Anomaly detected: {new_features[-1]}")

# Start capturing packets
def start_capture():
    for packet in capture.sniff_continuously():
        real_time_detection(packet)

# Initialize and start threads
if __name__ == '__main__':
    # Initial training with first batch of data
    capture.sniff(timeout=10)
    start_time = time.time()
    for packet in capture:
        process_packet(packet, features)
        if time.time() - start_time >= 60:
            break

    model = train_model(features)

    # Start the real-time capture and detection thread
    capture_thread = threading.Thread(target=start_capture)
    capture_thread.start()

    # Start the model update thread
    update_thread = threading.Thread(target=update_model)
    update_thread.start()

    capture_thread.join()
    update_thread.join()
