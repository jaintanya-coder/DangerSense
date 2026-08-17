# DangerSense 🛡️

### AI-Based Multi-Hazard CCTV Monitoring & Incident Response System

DangerSense is a real-time computer vision system that turns passive CCTV footage into an intelligent safety monitoring system.

It detects **fire, smoke, falls, person presence, and restricted-zone entry**, verifies events across multiple frames, and uses an **Incident Agent** for risk assessment and response decisions.

---

## 🚨 Problem Statement

Traditional CCTV systems rely on a person continuously watching the footage. This makes it difficult to notice incidents in homes, offices, businesses, storage areas, and restricted locations.

DangerSense adds an AI monitoring layer that automatically detects, verifies, evaluates, and records potentially dangerous events.

---

## ✨ Features

- 👤 **Person Detection** — YOLO-based person detection.
- 🔥 **Fire Detection** — Custom YOLO fire detection model.
- 💨 **Smoke Detection** — Detects smoke as part of hazard assessment.
- 🧍 **Fall Detection** — Pose-based analysis with temporal confirmation.
- 🚧 **Restricted Zone Detection** — Detects people entering configurable areas.
- ⏱️ **Temporal Confirmation** — Requires multiple consecutive frames before confirming an event.
- 🤖 **Incident Agent** — Evaluates confirmed incidents and selects appropriate responses.
- 🧠 **Risk Assessment** — Generates risk scores and severity levels.
- 📸 **Evidence Capture** — Saves evidence images for confirmed incidents.
- 📋 **Incident Logging** — Stores event, risk, reason, timestamp, and evidence.
- 📊 **Streamlit Dashboard** — Displays live feed, status, risk, and incident history.
- ⛔ **System Control** — Dashboard can stop the monitoring process.

---

## 🧠 System Architecture

```text
CCTV / Camera
      ↓
Frame Capture
      ↓
Computer Vision Detection
      ↓
Temporal Confirmation
      ↓
Incident Agent
      ↓
Risk Assessment
      ↓
Response Policy
      ↓
Action Executor
   ┌──┴──────────────┐
   ↓                 ↓
Evidence          Event Log
Capture
   └────────┬────────┘
            ↓
     Streamlit Dashboard
```

---

## 🤖 Incident Agent

The Incident Agent adds a decision-making layer after event confirmation.

```text
Confirmed Event
      ↓
Incident Classification
      ↓
Risk Factors
      ↓
Risk Score
      ↓
Severity
      ↓
Response Policy
      ↓
Selected Actions
```

Risk levels:

```text
80–100 → CRITICAL
50–79  → HIGH
25–49  → MEDIUM
0–24   → LOW
```

Possible actions include:

- `LOG_EVENT`
- `CAPTURE_EVIDENCE`
- `GENERATE_ALERT`
- `CONTINUE_MONITORING`
- `ESCALATE`

---

## 🛠️ Tech Stack

- Python
- OpenCV
- Ultralytics YOLO
- YOLO Pose Estimation
- NumPy
- Streamlit
- JSON

---

## 📁 Project Structure

```text
DangerSense/
│
├── alerts/
│   ├── alert_manager.py
│   └── event_logger.py
│
├── agent/
│   ├── incident_agent.py
│   ├── incident_state.py
│   ├── incident_memory.py
│   ├── response_policy.py
│   └── action_executor.py
│
├── client/
│   └── dashboard.py
│
├── config/
│   └── settings.py
│
├── detection/
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
│   ├── event_tracker.py
│   └── status_manager.py
│
├── outputs/
├── risk/
│   └── risk_assessment.py
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd DangerSense

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶️ Running DangerSense

Run both commands from the **DangerSense project root**.

### Terminal 1 — AI Monitoring

```bash
python main.py
```

### Terminal 2 — Dashboard

```bash
python -m streamlit run client/dashboard.py
```

Dashboard:

```text
http://localhost:8501
```

---

## 🎯 Configuration

Restricted-zone coordinates and detection settings can be configured in:

```text
config/settings.py
```

Example:

```python
ZONE_X1 = 20
ZONE_Y1 = 30
ZONE_X2 = 320
ZONE_Y2 = 450

CONFIRMATION_FRAMES = 8
```

An event must persist for the configured number of consecutive frames before it becomes a confirmed incident.

---

## 📸 Runtime Outputs

Generated runtime data is stored inside:

```text
outputs/
```

This includes:

- Latest processed frame
- Incident screenshots
- Current system status
- Event logs
- Stop-control file

Runtime files are excluded from version control using `.gitignore`.

---

## 🎯 Example Use Cases

### 🏠 Home Safety
Detects potential falls or hazards when nobody is actively watching the camera.

### 🔥 Fire Safety
Detects fire/smoke and evaluates whether a person may be exposed to the hazard.

### 🔐 Restricted Areas
Detects unauthorized entry into configured sensitive areas.

---

## ⚠️ Limitations

DangerSense is a **student capstone prototype** and is not intended to replace professional security or fire-safety systems.

Limitations include:

- Accuracy depends on camera quality and positioning.
- Fire/smoke detection depends on model training data.
- Fall detection can be affected by camera angle and occlusion.
- Restricted zones depend on configured coordinates.
- Computer vision models can produce false positives or false negatives.
- The current system focuses on a single-camera environment.

---

## 🔮 Future Improvements

- Multi-camera support
- Person tracking
- Mobile push notifications
- SMS/email alerts
- Cloud incident storage
- Improved fall detection
- Larger fire/smoke datasets
- Edge-device deployment
- Advanced incident analytics

---

## 🎓 Project Type

**AI-ML Cohort Capstone Project**

Focused on real-time computer vision, safety monitoring, risk assessment, and agent-assisted incident response.

---

## 👩‍💻 Author

**Tanya Jain**

B.Tech — Indira Gandhi Delhi Technical University for Women (IGDTUW)
