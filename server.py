import cv2
import numpy as np
from flask import Flask, jsonify
import os

app = Flask(__name__)

def detect_empty_slots(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    slots = [(50, 50, 100, 200), (200, 50, 100, 200)]  # Example coordinates
    empty_slots = 0
    for (x, y, w, h) in slots:
        slot_img = gray[y:y+h, x:x+w]
        _, threshold = cv2.threshold(slot_img, 128, 255, cv2.THRESH_BINARY)
        white_pixel_count = np.sum(threshold == 255)
        if white_pixel_count > 10000:  # Adjust threshold_value based on your parking slot size
            empty_slots += 1
    return len(slots) - empty_slots

def capture_image():
    cap = cv2.VideoCapture(0)  # Change the index if you have multiple cameras
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('current_parking.jpg', frame)
    cap.release()

@app.route('/parking_status')
def parking_status():
    capture_image()
    image_path = 'current_parking.jpg'
    slots_empty = detect_empty_slots(image_path)
    return jsonify({"empty_slots": slots_empty})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
