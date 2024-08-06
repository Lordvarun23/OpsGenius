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
import pickle

# Global variables
features = []
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

# Train model locally on client data
def train_local_model(features):
    df = preprocess_features(features)
    feature_columns = ['src_port', 'dst_port', 'protocol', 'length', 'inter_arrival_time']
    local_model = IsolationForest(contamination=0.01)
    local_model.fit(df[feature_columns])
    return local_model


from sklearn.ensemble import IsolationForest


def federated_averaging(models):
    # Assuming models is a list of IsolationForest models
    n_models = len(models)

    if n_models == 0:
        return None

    # Average the parameters of the models
    combined_model = IsolationForest()
    combined_model.estimators_ = []

    for i in range(len(models[0].estimators_)):
        avg_tree = np.mean([model.estimators_[i].tree_ for model in models], axis=0)
        combined_model.estimators_.append(avg_tree)

    return combined_model

import pickle

def save_model(model, filename='federated_model.pkl'):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)


# Global variables for federated learning
local_models = []
rounds = 5

# Capture network traffic
interface = 'Wi-Fi'
capture = pyshark.LiveCapture(interface=interface)


# Start capturing packets and training local models
def start_capture():
    for round_num in range(rounds):
        # Capture packets for a fixed duration
        capture.sniff(timeout=6)
        features = []
        for packet in capture:
            process_packet(packet, features)

        # Train local model
        local_model = train_local_model(features)
        local_models.append(local_model)

        # Perform federated averaging
        global_model = federated_averaging(local_models)

        # Save the global model
        save_model(global_model)

        print(f"Round {round_num + 1}/{rounds} completed. Model saved.")


if __name__ == '__main__':
    start_capture()
