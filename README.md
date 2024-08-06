# IT-Operations-Network-Monitoring

## Files:
  1. ContinousAnomalyDetect - This application **continously monitors** the **network packets** and flags it as **anomaly** using **Isolation Forest** algorithm trained on **Federated Learning** methodology to preserve **Data privacy and Security**. Also, re-training pipeline is implemented after fixed interval specified by the user. Writes the flagged packet to csv file.
  2. FL_AnomalyDetect - This application trains the anomaly detection algorithm on **Federated learning methodology**.
  3. app.py - This is the main application based on **flask**, This **generates a data** for the IT assets, Network performance etc and shows network chatbot, displays csv file.
  4. ITOpsDashboard - **Dash based dahsboard** to display various metrics such as IT assets, Network Performance, IT operations etc.
  5. IT Service Ticket Classification - This application tries to **classify each raised ticket** into several issues such as Hardware, Access, IT Support, HR etc.
  6. Network Monitoring Chatbot - **Mistal 7B based function calling LLM** where user can ask queries to monitor the network in plain english and LLM returns back the result by calling the appropriate function.

## Packages to Install
  1. Install wireshark application
  2. pip install pyshark, plotly, flask, scikit-learn, ping3, transformers, torch, locale, langchain, langchain-community, bitsandbytes accelerate  langchain-core
     
## Steps to run 
1. execute ContinousAnomalyDetect, ITOpsDashboard, app.py in this order

## Results
### Homepage
![image](https://github.com/user-attachments/assets/ba75f127-153e-49ad-9adb-8abfeb84b9a0)

### IT Ops Dashboard
![image](https://github.com/user-attachments/assets/df98e447-94af-4e0e-8614-3783a3ed9013)

### Network Monitoring chatbot
![image](https://github.com/user-attachments/assets/a48646f1-1f0d-4e81-b809-1ffc2038738c)
![image](https://github.com/user-attachments/assets/87a196d9-414f-4d1d-a2ba-9f293b912fe0)
![image](https://github.com/user-attachments/assets/6708877f-8184-45bc-9d15-6243a2df34d8)

### IT Service Ticket Classification
![image](https://github.com/user-attachments/assets/15fe632c-1018-4f6e-8adf-088b687d26c5)

### Network Packet Anomaly Detection
![image](https://github.com/user-attachments/assets/c4114a75-dc6b-4d17-b9af-fedc31e8f09e)









