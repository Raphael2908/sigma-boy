import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import math
import os


# ---------------------- Helper Functions -------------------------

def distance(point1, point2, image_shape):
    ih, iw = image_shape
    x1, y1 = int(point1.x * iw), int(point1.y * ih)
    x2, y2 = int(point2.x * iw), int(point2.y * ih)
    return math.hypot(x2 - x1, y2 - y1)

def draw_face_landmarks(image):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)
    drawing_spec = mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)

    image_np = np.array(image.convert('RGB'))
    results = face_mesh.process(image_np)

    if results.multi_face_landmarks:
        annotated_image = image_np.copy()
        for face_landmarks in results.multi_face_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_spec)

            # Draw jawline in green
            jaw_indices = list(range(0, 17))
            h, w, _ = image_np.shape
            jaw_points = [(int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)) for i in jaw_indices]
            cv2.polylines(annotated_image, [np.array(jaw_points)], isClosed=False, color=(0, 255, 0), thickness=2)

            # Draw bounding box
            x_coords = [int(lm.x * w) for lm in face_landmarks.landmark]
            y_coords = [int(lm.y * h) for lm in face_landmarks.landmark]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            cv2.rectangle(annotated_image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

        return annotated_image, results.multi_face_landmarks[0].landmark
    else:
        return None, None

def classify_face_shape(landmarks, image_shape):
    jaw_width = distance(landmarks[0], landmarks[16], image_shape)
    cheekbone_width = distance(landmarks[234], landmarks[454], image_shape)
    face_height = distance(landmarks[10], landmarks[152], image_shape)

    ratio1 = face_height / cheekbone_width if cheekbone_width else 0
    ratio2 = cheekbone_width / jaw_width if jaw_width else 0

    if ratio1 > 1.5:
        return "Long"
    elif ratio1 < 1.2 and ratio2 > 1.05:
        return "Round"
    elif 1.2 <= ratio1 <= 1.5 and 0.9 <= ratio2 <= 1.05:
        return "Oval"
    else:
        return "Square"

def recommend_exercises():
    return [
        {"name": "Mewing", "duration": "10 mins/day", "description": "Tongue posture to define jawline."},
        {"name": "Chin Lifts", "duration": "5 mins/day", "description": "Stretch chin upward repeatedly."},
        {"name": "Fish Face", "duration": "5 mins/day", "description": "Suck cheeks in and hold."}
    ]