from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
import os
import pandas as pd
import cv2
import numpy as np
import threading
from datetime import datetime, timedelta
import platform
import subprocess

app = Flask(__name__)

# Config
BASE_DIR = os.getcwd()
ATTENDANCE_DIR = os.path.join(BASE_DIR, "attendance")
USERS_FILE = os.path.join(BASE_DIR, "users.csv")
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
TRAINER_PATH = os.path.join(BASE_DIR, "trainer", "face_trainer.yml")
CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")

# Core AI Setup
recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8, threshold=80.0)
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
camera = None
is_scanning = False
last_marked = {} # {username: time} cooldown

os.makedirs(ATTENDANCE_DIR, exist_ok=True)
os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "trainer"), exist_ok=True)

COLLEGE_WIFI_SSIDS = ["NetDonar"]

def get_connected_wifi():
    system = platform.system()
    try:
        if system == "Windows":
            output = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], stderr=subprocess.DEVNULL).decode()
            for line in output.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()
    except: return None
    return None

def on_prescribed_wifi():
    ssid = get_connected_wifi()
    return ssid in COLLEGE_WIFI_SSIDS

# Routes
@app.route('/')
def about(): return render_template('about.html')

@app.route('/login')
def login(): return render_template('login.html')

@app.route('/dashboard')
def dashboard(): return render_template('dashboard.html')

# Video Streaming
@app.route('/video_feed')
def video_feed():
    global is_scanning
    is_scanning = True
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    global camera, is_scanning
    if camera is None: camera = cv2.VideoCapture(0)
    
    if os.path.exists(TRAINER_PATH): recognizer.read(TRAINER_PATH)
    label_map = sorted([d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))])

    while is_scanning:
        success, frame = camera.read()
        if not success: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            name, score = "Unknown", 0
            if os.path.exists(TRAINER_PATH):
                id_num, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                score = round(max(0, 100 - confidence))
                if score >= 70 and id_num < len(label_map):
                    name = label_map[id_num]
                    mark_attendance_internal(name)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (56, 189, 248), 2)
            cv2.putText(frame, f"{name} ({score}%)", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (56, 189, 248), 2)
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def mark_attendance_internal(name):
    now = datetime.now()
    if name in last_marked and (now - last_marked[name]).seconds < 300: return
    date_str = now.strftime("%Y-%m-%d")
    file_path = os.path.join(ATTENDANCE_DIR, f"attendance_{date_str}.csv")
    new_data = pd.DataFrame([{"Name": name, "Time": now.strftime("%H:%M:%S")}])
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if name not in df["Name"].values:
            pd.concat([df, new_data]).to_csv(file_path, index=False)
            last_marked[name] = now
    else:
        new_data.to_csv(file_path, index=False)
        last_marked[name] = now

# Authentication API
@app.route('/api/login', methods=['POST'])
def api_login():
    if not on_prescribed_wifi():
        return jsonify({"status": "error", "message": "Restricted Access: Network Geofence (NetDonar)"}), 403
    data = request.json
    users = pd.read_csv(USERS_FILE).to_dict('records') if os.path.exists(USERS_FILE) else []
    for u in users:
        if u['username'] == data['username'] and u['password'] == data['password'] and u['role'] == data['role']:
            return jsonify({"status": "success", "user": u})
    return jsonify({"status": "error", "message": "Invalid Login Credentials"}), 401

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if os.path.exists(USERS_FILE):
        df = pd.read_csv(USERS_FILE)
        if username in df['username'].values:
            return jsonify({"status": "error", "message": "Username already exists"}), 400
    else:
        df = pd.DataFrame(columns=['username', 'password', 'role'])
    
    new_user = pd.DataFrame([{"username": username, "password": password, "role": "student"}])
    pd.concat([df, new_user]).to_csv(USERS_FILE, index=False)
    return jsonify({"status": "success", "message": "Account created! Now login to register your face."})

@app.route('/api/check_registration/<username>')
def check_registration(username):
    user_dir = os.path.join(DATASET_DIR, username)
    registered = os.path.exists(user_dir) and len(os.listdir(user_dir)) > 0
    return jsonify({"registered": registered})

@app.route('/api/register/start', methods=['POST'])
def start_registration():
    username = request.json.get('username')
    def run_reg():
        subprocess.run(["python", "collect_faces_script.py", username])
        subprocess.run(["python", "train_model.py"])
    threading.Thread(target=run_reg, daemon=True).start()
    return jsonify({"status": "success"})

@app.route('/api/stats/<username>')
def get_stats(username):
    present, total = 0, 0
    if os.path.exists(ATTENDANCE_DIR):
        files = [f for f in os.listdir(ATTENDANCE_DIR) if f.startswith("attendance_")]
        total = len(files)
        for f in files:
            df = pd.read_csv(os.path.join(ATTENDANCE_DIR, f))
            if username in df["Name"].values: present += 1
    pct = round((present / total) * 100, 2) if total > 0 else 0
    return jsonify({"percentage": f"{pct}%", "total": total, "present": present})

@app.route('/api/admin/stats')
def get_admin_stats():
    label_map = sorted([d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))])
    return jsonify({"total_students": len(label_map), "system_status": "Secure"})

@app.route('/api/stop_scan')
def stop_scan():
    global is_scanning, camera
    is_scanning = False
    if camera: camera.release(); camera = None
    return jsonify({"status": "stopped"})

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
