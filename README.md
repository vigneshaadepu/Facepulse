<div align="center">

  <!-- Logo & Title -->
  <a href="https://github.com/your-username/FacePulse">
    <img src="https://img.shields.io/badge/FACEPULSE-BIOMETRIC%20AI%20ECOSYSTEM-00F2FE?style=for-the-badge&logo=opsgenie&logoColor=white" alt="FacePulse Banner" width="420"/>
  </a>

  <h1 align="center">💠 FacePulse</h1>
  <h3 align="center">Next-Generation Biometric Intelligence & Geofenced Attendance Ecosystem</h3>

  <p align="center">
    <strong>Automated Real-Time Presence Verification powered by OpenCV LBPH Neural Engine & Network-Aware Geofencing</strong>
  </p>

  <!-- Dynamic Typing Animation Banner -->
  <p align="center">
    <a href="https://github.com/readme-typing-svg">
      <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&pause=1000&color=38BDF8&center=true&vcenter=true&width=550&lines=⚡+0.2s+Neural+Biometric+Face+Matching;🌐+Hardware-Aware+Wi-Fi+Geofence+Lock;📊+Dual-Lobby+Web+%26+Desktop+Analytics;🔐+50-Frame+High-Res+Identity+Enrollment" alt="Typing SVG" />
    </a>
  </p>

  <!-- Shields & Badges Grid -->
  <p align="center">
    <a href="#-tech-stack"><img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.9+"></a>
    <a href="#-tech-stack"><img src="https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"></a>
    <a href="#-tech-stack"><img src="https://img.shields.io/badge/OpenCV-LBPH_v4.8-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV"></a>
    <a href="#-tech-stack"><img src="https://img.shields.io/badge/Interface-Web_%26_Desktop-00F2FE?style=for-the-badge&logo=electron&logoColor=black" alt="Web and Desktop"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="MIT License"></a>
  </p>

  <p align="center">
    <a href="#-product-overview">Overview</a> •
    <a href="#-key-features">Key Features</a> •
    <a href="#-system-architecture">Architecture</a> •
    <a href="#-tech-stack">Tech Stack</a> •
    <a href="#-installation--quickstart">Quickstart</a> •
    <a href="#-project-architecture">Structure</a>
  </p>

  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="Separator" />
</div>

<br/>

## 🎯 Product Overview

> [!IMPORTANT]
> **FacePulse** bridges computer vision biometrics with network-layer location assurance. Designed for modern corporate and academic environments, it replaces error-prone manual logs and static QR codes with a zero-friction, anti-proxy presence tracking engine.

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🔐 Neural Biometric Core</h3>
      <p>Utilizes <strong>Local Binary Patterns Histograms (LBPH)</strong> with 50-frame per-user facial identity sampling. Evaluates frame vectors at a strict <strong>70% confidence threshold</strong> to instantly eliminate proxy attempts while delivering sub-second matching.</p>
    </td>
    <td width="50%" valign="top">
      <h3>🌐 Hardware Network Geofencing</h3>
      <p>Implements native OS-level interface querying (<code>netsh wlan</code> integration) to restrict attendance authorization exclusively to verified organization Wi-Fi SSIDs (e.g. <code>NetDonar</code>), enforcing physical presence integrity.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>💻 Dual-Platform Portal</h3>
      <p>Features both a sleek <strong>Flask Glassmorphism 2.0 Web Application</strong> with dynamic Chart.js dashboards and a high-performance <strong>Tkinter Desktop Client</strong> with real-time dark/light theme switching and embedded Matplotlib telemetry.</p>
    </td>
    <td width="50%" valign="top">
      <h3>📈 Presence Intelligence</h3>
      <p>Automates daily and weekly attendance compilation into structured Pandas datasets with gamified engagement tracking (streaks, punctuality metrics) and anti-spam 300-second verification cooldowns.</p>
    </td>
  </tr>
</table>

<br/>

## ⚡ Key Features

| Capability | Engine / Feature | Description | Status |
| :--- | :--- | :--- | :---: |
| **Biometric Match** | `OpenCV LBPH` | Real-time face detection & 0.2s identity classification | `ACTIVE` |
| **Identity Training** | `50-Frame Mapping` | Automated multi-angle dataset collection & model synthesis | `ACTIVE` |
| **Geofence Lock** | `SSID Validation` | Native Wi-Fi network inspection to prevent remote spoofing | `ACTIVE` |
| **Web Portal** | `Flask + Glassmorphism` | Interactive scan popups, active status badges & student timeline | `ACTIVE` |
| **Desktop Suite** | `Tkinter + Matplotlib` | Native GUI client with dark/light themes & integrated graphs | `ACTIVE` |
| **Analytics Engine** | `Pandas + Chart.js` | Heatmaps, daily presence CSV generation & weekly summaries | `ACTIVE` |

<br/>

## 🏗️ System Architecture

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 User / Student
    participant Web as 🌐 Flask / GUI Front
    participant Network as 📶 Network Validator
    participant Camera as 📷 OpenCV Stream
    participant AI as 🧠 LBPH Engine
    participant DB as 📁 Attendance CSV

    User->>Web: Initiate "Mark Attendance"
    Web->>Network: Query Active Wi-Fi SSID
    alt SSID != Authorized Network (e.g. NetDonar)
        Network-->>Web: ❌ Access Denied (Geofence Lock)
        Web-->>User: Show Geofence Restriction Alert
    else Network Validated
        Network-->>Web: ✅ Network Verified
        Web->>Camera: Activate WebCam Frame Feed
        Camera->>AI: Pass Grayscale Frame Matrix
        AI->>AI: Detect Haar Cascade & Compute LBPH Match
        alt Confidence Score >= 70%
            AI->>DB: Log Name, Timestamp & Date (300s Cooldown)
            AI-->>Web: Return Match Signal & User Profile
            Web-->>User: Display Biometric Verification Success
        else Confidence Score < 70% / Unknown
            AI-->>Web: Return Unknown Identity
            Web-->>User: Flag Unrecognized Biometric
        end
    end
```

<br/>

## 🛠️ Tech Stack

<div align="center">

| Domain | Technologies & Frameworks |
| :--- | :--- |
| **Core AI & Vision** | ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white) ![Haar Cascade](https://img.shields.io/badge/Haar%20Cascade-Face%20Detection-blue?style=flat-square) |
| **Backend & APIs** | ![Python](https://img.shields.io/badge/Python%203.9+-3776AB?style=flat-square&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white) |
| **Frontend Web** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) ![CSS3 Glassmorphism](https://img.shields.io/badge/CSS3-Glassmorphism%202.0-1572B6?style=flat-square&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript%20ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black) |
| **Desktop App** | ![Tkinter](https://img.shields.io/badge/Tkinter-GUI%20Toolkit-3776AB?style=flat-square) ![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c?style=flat-square) |
| **UI Libraries** | ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat-square&logo=chartdotjs&logoColor=white) ![SweetAlert2](https://img.shields.io/badge/SweetAlert2-Sleek%20Modals-red?style=flat-square) ![FontAwesome](https://img.shields.io/badge/FontAwesome%206-528DD7?style=flat-square&logo=fontawesome&logoColor=white) |

</div>

<br/>

## 📊 Performance & Security Benchmarks

> [!NOTE]
> Engineered to run efficiently on standard workstation hardware without requiring specialized TPU/GPU accelerators.

- **Neural Detection Latency**: `~200ms per frame`
- **Biometric Enrollment Matrix**: `50 normalized facial keyframes per user`
- **Verification Confidence Threshold**: `70% matching threshold (100 - distance)`
- **Network Verification Overhead**: `< 15ms local SSID inspection`
- **Attendance Record Cooldown**: `300 seconds (prevents duplicate logs)`

<br/>

## 🚀 Installation & Quickstart

### Prerequisites

- Python **3.9** or higher
- System webcam / integrated camera
- OpenCV dependencies (`opencv-contrib-python`)

### 1️⃣ Clone & Setup Environment

```bash
# Clone the repository
git clone https://github.com/your-username/FacePulse.git
cd FacePulse

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requriments.txt
```

> [!TIP]
> Ensure `haarcascade_frontalface_default.xml` is located in the root directory before running the system.

### 3️⃣ Train Biometric Model & Launch

#### Option A: Launch Web Portal (Flask)
```bash
python app.py
```
*Access the interactive portal at `http://127.0.0.1:5000`*

#### Option B: Launch Desktop Application (Tkinter GUI)
```bash
python gui.py
```

<br/>

## 📂 Project Architecture

```
FacePulse/
├── 📄 app.py                  # Main Flask server, streaming endpoint & geofence routing
├── 📄 gui.py                  # Tkinter Desktop application with dark/light themes & charts
├── 📄 collect_faces.py        # OpenCV biometric face sample collector engine
├── 📄 collect_faces_script.py # Automated identity capture script (50 frames)
├── 📄 train_model.py          # LBPH model trainer & weights compiler
├── 📄 recognize_attendance.py # Standalone attendance recognition pipeline
├── 📄 daily_report.py         # Daily presence log summary generator
├── 📄 weekly_report.py        # Weekly attendance metrics & analytics generator
├── 📄 test_camera.py          # Optical camera diagnostic utility
├── 📁 attendance/             # Auto-generated daily CSV presence logs
├── 📁 dataset/                # Biometric identity image nodes per user
├── 📁 trainer/                # Compiled face recognition weights (face_trainer.yml)
├── 📁 static/                 # Web assets (Glassmorphism CSS, JS, logo images)
├── 📁 templates/              # HTML5 application views (about, login, dashboard)
└── 📄 haarcascade_frontalface_default.xml # Haar Cascade face detector classifier
```

<br/>

## 🔄 User Workflow

```
[ 1. User Enrollment ] ────► Captures 50 face samples via OpenCV camera engine
                                           │
                                           ▼
[ 2. Neural Training ] ────► Compiles dataset into trainer/face_trainer.yml
                                           │
                                           ▼
[ 3. Network Check  ] ────► Verifies active SSID against authorized Wi-Fi list
                                           │
                                           ▼
[ 4. Presence Scan  ] ────► 0.2s LBPH face recognition matching (>=70% score)
                                           │
                                           ▼
[ 5. Log & Analytics] ────► Appends entry to CSV log + updates dynamic dashboards
```

<br/>

## ⚖️ License & Acknowledgements

This project is licensed under the **MIT License**.

<div align="center">
  <br/>
  <p><strong>FacePulse — Designed for the Future of Secure Biometric Automation</strong></p>

  <a href="#-facepulse"><img src="https://img.shields.io/badge/↑_Back_To_Top-00F2FE?style=for-the-badge&logo=spacex&logoColor=black" alt="Back to top"></a>
  <br/><br/>
</div>
