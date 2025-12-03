# Hand Tracking POC - Arvyax Internship Assignment

## Overview
This project is a prototype for real-time hand tracking and interaction with a virtual object using classical computer vision techniques (without MediaPipe/OpenPose).  
The system detects the hand, tracks its position, and triggers visual warnings based on distance to a virtual object.

## Features
- Real-time hand tracking using contour detection
- Virtual object displayed on screen
- Dynamic state logic:
  - SAFE: hand far from object (green)
  - WARNING: hand approaching object (yellow)
  - DANGER: hand very close / touching object (red) + "DANGER DANGER" overlay
- Runs on CPU with real-time performance (~8 FPS+)

## Requirements
- Python 3.x
- OpenCV
- NumPy

Install dependencies:
```bash
pip install -r requirements.txt
# hand_tracking_poc
Internship project
