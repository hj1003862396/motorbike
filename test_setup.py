#!/usr/bin/env python3
"""
Test script to verify the motorbike detection project setup
"""
import sys
sys.path.insert(0, '/Users/hanjie/PycharmProjects/Motorbike-detection')

import cv2
import numpy as np
import datetime
from object_detection import ObjectDetection
from deep_sort_wrapper import Deep
from grid import RectangularArea, CheckTool

print("=" * 60)
print("Motorbike Detection Project - Setup Test")
print("=" * 60)

# Step 1: Load Object Detection
print("\n[1/4] Loading YOLOv4 model...")
try:
    od = ObjectDetection("yolov4.weights", "yolov4.cfg")
    od.load_class_names("coco.names")
    od.load_detection_model(image_size=416, nmsThreshold=0.4, confThreshold=0.3)
    print("✓ YOLOv4 model loaded successfully")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    sys.exit(1)

# Step 2: Load Deep Sort Tracker
print("\n[2/4] Loading Deep Sort tracker...")
try:
    deep = Deep(max_distance=0.7, nms_max_overlap=1, n_init=3, max_age=15, max_iou_distance=0.7)
    tracker = deep.sort_tracker()
    print("✓ Deep Sort tracker loaded successfully")
except Exception as e:
    print(f"✗ Error loading tracker: {e}")
    sys.exit(1)

# Step 3: Load mask and video
print("\n[3/4] Loading mask and video source...")
try:
    mask = cv2.imread("new_mask.jpeg")
    if mask is None:
        print("⚠ Mask file not found, will use full frame")
    else:
        print(f"✓ Mask loaded: {mask.shape}")

    cap = cv2.VideoCapture("xemay_xoay_ngang_lan.mp4")
    if not cap.isOpened():
        print("⚠ Video file not found, using webcam (index 0)")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("✗ Cannot open webcam")
            sys.exit(1)
    print("✓ Video source opened successfully")
except Exception as e:
    print(f"✗ Error loading video: {e}")
    sys.exit(1)

# Step 4: Test detection on a sample frame
print("\n[4/4] Testing detection on sample frame...")
try:
    ret, frame = cap.read()
    if not ret:
        print("✗ Cannot read frame from video source")
        sys.exit(1)

    print(f"✓ Frame captured: {frame.shape}")

    # Apply mask if available
    if mask is not None:
        frame_region = cv2.bitwise_and(frame, mask)
    else:
        frame_region = frame

    # Run detection
    (class_ids, scores, boxes) = od.detect(frame_region)
    print(f"✓ Detection completed: {len(boxes)} objects detected")

    # Run tracking
    features = deep.encoder(frame_region, boxes)
    detections = deep.Detection(boxes, scores, class_ids, features)
    tracker.predict()
    (class_ids, object_ids, boxes) = tracker.update(detections)
    print(f"✓ Tracking completed: {len(object_ids)} objects tracked")

except Exception as e:
    print(f"✗ Error during detection: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

cap.release()

print("\n" + "=" * 60)
print("✓ All tests passed! Project is ready to run.")
print("=" * 60)
print("\nTo run the full project:")
print("  python3 motorbike_project.py")
print("\nNote: The project will use webcam if video file is not found.")
print("      Press ESC to exit the application.")
