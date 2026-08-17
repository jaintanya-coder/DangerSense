# DangerSense 🛡️

### AI-Based Multi-Hazard CCTV Monitoring System

DangerSense is a real-time computer vision system designed to turn passive CCTV footage into an intelligent safety monitoring system.

Instead of requiring a person to continuously watch a camera feed, DangerSense analyzes the footage and identifies potentially dangerous events such as **fire, smoke, falls, and unauthorized entry into restricted areas**.

The system verifies detected events across multiple consecutive frames before treating them as confirmed incidents, helping reduce false alerts caused by single-frame detections.

---

## 🚨 Problem Statement

Traditional CCTV systems continuously record video, but they generally depend on a human operator to notice important events.

This creates a problem in places such as:

- Homes
- Small businesses
- Offices
- Storage areas
- Restricted rooms
- Other locations where continuous monitoring is difficult

DangerSense acts as an **AI monitoring layer over a CCTV camera** and brings potentially important events to the user's attention.

---

## ✨ Features

### 👤 Person Detection

Detects people present in the camera frame using YOLO-based object detection.

### 🔥 Fire Detection

Detects visible fire using a custom-trained YOLO model.

### 💨 Smoke Detection

Detects smoke and distinguishes it from normal scene activity.

### 🧍 Fall Detection

Uses pose estimation and body-position analysis to identify potential falls.

The system considers:

- Body orientation
- Shoulder and hip positions
- Downward movement
- Temporal persistence

This helps distinguish potential falls from simple sitting or bending.

### 🚧 Restricted Zone Detection

A configurable region of the camera frame can be marked as a restricted area.

If a detected person enters this area, the system generates a security incident.

### ⏱️ Temporal Event Confirmation

The system does not immediately treat every individual detection as a confirmed incident.

An event must remain present across multiple consecutive frames before being confirmed.

This reduces false alerts caused by temporary detection errors.

### 📸 Evidence Capture

When an incident is confirmed, DangerSense captures an image of the event.

### 📋 Incident Logging

Confirmed incidents are recorded with information such as:

- Event type
- Risk level
- Reason
- Timestamp
- Evidence image

### 📊 Monitoring Dashboard

A Streamlit dashboard provides a simple interface for viewing the current monitoring status and recorded incidents.

### ⛔ System Control

The dashboard includes a stop control that signals the monitoring process to stop and closes the camera feed.

---

## 🧠 System Architecture

```text
                    CCTV / Camera
                          │
                          ▼
                ┌──────────────────┐
                │   Frame Capture  │
                └────────┬─────────┘
                         │
                         ▼
             ┌────────────────────────┐
             │ Computer Vision Models │
             ├────────────────────────┤
             │ Person Detection       │
             │ Fire Detection         │
             │ Smoke Detection        │
             │ Pose / Fall Detection  │
             └───────────┬────────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Risk Assessment  │
                └────────┬─────────┘
                         │
                         ▼
             ┌────────────────────────┐
             │ Temporal Confirmation  │
             └───────────┬────────────┘
                         │
                  Confirmed Event
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      Evidence Capture         Event Logging
             │                       │
             └───────────┬───────────┘
                         ▼
                Streamlit Dashboard
```

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV**
- **Ultralytics YOLO**
- **YOLO Pose Estimation**
- **NumPy**
- **Streamlit**

---

## 📁 Project Structure

```text
DangerSense/
│
├── alerts/
│   ├── __init__.py
│   ├── alert_manager.py
│   └── event_logger.py
│
├── client/
│   ├── __init__.py
│   └── dashboard.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── detection/
│   ├── __init__.py
│   ├── person_detector.py
│   ├── fire_detector.py
│   ├── fall_detector.py
│   └── restricted_zone.py
│
├── models/
│   ├── best.pt
│   ├── yolo11n.pt
│   └── yolo11n-pose.pt
│
├── monitoring/
│   ├── __init__.py
│   ├── event_tracker.py
│   └── status_manager.py
│
├── outputs/
│   └── .gitkeep
│
├── risk/
│   ├── __init__.py
│   └── risk_assessment.py
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd DangerSense
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

On Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running DangerSense

DangerSense uses two processes: the **AI monitoring system** and the **Streamlit dashboard**.

### Terminal 1 — Start the AI Monitoring System

```bash
python main.py
```

This starts the camera and runs the computer vision pipeline.

### Terminal 2 — Start the Dashboard

```bash
streamlit run client/dashboard.py
```

The Streamlit dashboard will open in the browser.

---

## 🎯 Configuring the Restricted Zone

The restricted area can be configured from:

```text
config/settings.py
```

Example:

```python
ZONE_X1 = 20
ZONE_Y1 = 30
ZONE_X2 = 320
ZONE_Y2 = 450
```

The coordinates can be adjusted according to the camera resolution and the desired restricted region.

---

## ⏱️ Event Confirmation

DangerSense uses temporal confirmation instead of treating every individual model prediction as an incident.

For example:

```text
Frame 1  → Possible event
Frame 2  → Possible event
Frame 3  → Possible event
   ...
Frame 8  → Confirmed event
```

Only after an event persists across the required number of consecutive frames is it treated as a confirmed incident.

This helps reduce false alerts caused by temporary model predictions.

---

## 📸 Evidence and Event Logs

Runtime-generated files are stored in:

```text
outputs/
```

These may include:

- Incident screenshots
- Latest processed frame
- Event logs
- Runtime control files

Generated runtime data is excluded from version control using `.gitignore`.

---

## ⚠️ Limitations

DangerSense is a student capstone prototype and is **not intended to replace professional security or fire-safety systems**.

Potential limitations include:

- Detection accuracy depends on camera quality and positioning.
- Fire and smoke detection depends on the training data of the custom model.
- Pose-based fall detection can be affected by camera angle, occlusion, and multiple people.
- Restricted-zone detection is based on configured camera coordinates.
- The system currently focuses on a controlled single-camera environment.

---

## 🔮 Future Improvements

Possible future improvements include:

- Multi-camera support
- Person tracking across frames
- Mobile push notifications
- SMS / email alerts
- More robust multi-person fall tracking
- Cloud-based incident storage
- Improved fire and smoke datasets
- Edge-device deployment

---

## 🎓 Project Type

This project was developed as a **AI-ML cohort capstone project** focused on real-time safety monitoring.

---

## 👩‍💻 Author

**Tanya Jain**

B.Tech — Indira Gandhi Delhi Technical University for Women (IGDTUW)
