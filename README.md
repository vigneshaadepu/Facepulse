# 💠 FacePulse: The AI-Powered Biometric Ecosystem

**FacePulse** is a cutting-edge, high-security attendance system that leverages advanced facial recognition and geofencing technology to automate presence tracking in professional and academic environments.

![FacePulse Logo](/static/img/logo.png)

## 🚀 Key Features

### 🔐 Biometric Intelligence
- **0.2s Neural Matching**: Lightning-fast face detection using optimized LBPH (Local Binary Patterns Histograms).
- **Quantum-Glass Portal**: A modern, interactive web interface featuring real-time biometric scan popups.
- **70% Confidence Threshold**: Ensures high-accuracy verification, preventing proxy attendance.

### 🌐 Secure Geofencing
- **Network Lock**: Attendance marking is restricted to authorized campus Wi-Fi networks (e.g., `NetDonar`).
- **Real-time Sync Badge**: Constant monitoring of the geofence signal to maintain system integrity.

### 📊 Engagement-Rich Dashboard
- **Neural Metric Overlook**: Interactive line charts visualizing engagement stability and presence density.
- **Attendance Heatmap**: Grid-based visualization of frequency and consistency.
- **Weekly Academic Timeline**: Integrated schedule module for personalized student tracking.
- **Performance Badges**: Gamified rewards (e.g., "Punctuality King", "7-Day Streak") to boost user engagement.

### 👤 Identity Management
- **Neural Mapping**: Mandatory 50-frame face enrollment for new users to establish a high-resolution biometric profile.
- **Dual Lobby Architecture**: Dedicated student signup and secure admin-only authentication.

---

## 🛠️ Technology Stack

- **Backend**: Python (Flask, OpenCV, Pandas, Numpy)
- **Frontend**: HTML5, CSS3 (Glassmorphism 2.0), JavaScript (Vanilla ES6)
- **Visuals**: Chart.js, AOS (Animate on Scroll), SweetAlert2, Font-Awesome 6.0
- **Biometrics**: OpenCV LBPH (Neural Face Recognition)

---

## ⚙️ Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/FacePulse.git
   cd FacePulse
   ```

2. **Install Dependencies**:
   ```bash
   pip install flask opencv-contrib-python pandas numpy
   ```

3. **Initialize the Environment**:
   - Ensure you have a webcam connected.
   - Place a `haarcascade_frontalface_default.xml` in the root directory.

4. **Launch the Portal**:
   ```bash
   python app.py
   ```
   *Access the interface at [http://127.0.0.1:5000](http://127.0.0.1:5000)*

---

## 🤝 Usage Workflow

### For Students
1. **Enrollment**: Sign up via the Portal lobby.
2. **Profile Sync**: Create your "Neural Signature" (Face Registration) upon first login.
3. **Verification**: Enter the **Mark Presence** section and launch the **Biometric Scan** popup to log your attendance.

### For Administrators
1. **Access Control**: Login via the pre-configured admin credentials.
2. **Data Decryption**: Perform a biometric handshake to unlock the system-wide student presence directory and analytics.

---

## 📂 Project Architecture

```
FacePulse/
├── app.py                  # Main Flask Server & Recognition API
├── collect_faces_script.py  # AI Face Data Collection Engine
├── train_model.py          # Neural Network Training Script
├── attendance/             # Encrypted Presence Logs (CSV)
├── dataset/                # Biometric Identity Nodes
├── trainer/                # Compiled AI Models (.yml)
├── static/                 # Branding & Dynamic Assets (CSS/JS/Img)
└── templates/              # High-End Portal Views (HTML)
```

---

## ⚖️ License & Credits

FacePulse is a proprietary product of **AI Biometric Labs**. Licensed under the **MIT License**.

&copy; 2026 AI Biometric Labs. Designed for the Future of Security.
