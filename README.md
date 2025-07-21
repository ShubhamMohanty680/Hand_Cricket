# 🏏 Gesture-Controlled Cricket Game 🎮

A **gesture-based virtual cricket game** where players can bat and bowl using **hand gestures via webcam** — no keyboard or controller needed! Built using **MediaPipe**, **OpenCV**, and a **custom-trained Random Forest model**.


## 🎯 Features

- ⚡ Real-time gesture recognition using webcam
- 🤝 Two-player interactive gameplay
- 🧠 Machine learning model trained on hand landmarks
- 🕹️ Toss logic with batting or bowling decision
- 🏏 Two full innings, including out detection
- 📊 Automatic match result computation

---

## 🧠 How It Works

1. **Hand Gesture Recognition**: MediaPipe detects hand landmarks; the model classifies gestures into `0`, `1`, `2`, `3`, `4`, `6`, or `closed`.
2. **Toss**: One player calls head/tail, toss is simulated.
3. **Bat/Bowl Choice**: Toss winner chooses to bat or bowl.
4. **Gameplay**:
   - Both players show their gesture simultaneously.
   - If gestures match → **OUT**
   - Else → Runs are added from batter’s gesture.
   - Game plays for up to 6 valid inputs or until batter gets out.

---

## 🛠️ Tech Stack

- Python 🐍
- MediaPipe ✋ (Hand tracking)
- OpenCV 🎥 (Camera feed + annotations)
- Scikit-learn 🤖 (Random Forest Classifier)
- Multiprocessing 🔁 (Simultaneous gesture capture from 2 players)

## Installation

1. Cloning the repository
``` python
git clone https://github.com/your-username/gesture-cricket.git
cd gesture-cricket
```
2. Creating and activating the environment
``` python
# Create a virtual environment 
python -m venv env

# Activate it
source env/bin/activate

```
3. Installing the dependencies
``` python
pip install -r requirements.txt
```

4. Running the game
``` python
python app.py
```
