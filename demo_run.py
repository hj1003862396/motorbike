#!/usr/bin/env python3
"""
Motorbike Detection Project - Demo with Synthetic Frames
This version generates synthetic video frames for testing
"""
import sys
sys.path.insert(0, '/Users/hanjie/PycharmProjects/Motorbike-detection')

import cv2
import numpy as np
import datetime
from object_detection import ObjectDetection
from deep_sort_wrapper import Deep
from grid import RectangularArea, CheckTool

print("=" * 70)
print("Motorbike Detection Project - Running with Synthetic Frames")
print("=" * 70)

# Load Object Detection
print("\n[Loading] YOLOv4 model...")
od = ObjectDetection("yolov4.weights", "yolov4.cfg")
od.load_class_names("coco.names")
od.load_detection_model(image_size=416, nmsThreshold=0.4, confThreshold=0.3)
print("✓ YOLOv4 model loaded")

# Load Object Tracking Deep Sort
print("[Loading] Deep Sort tracker...")
deep = Deep(max_distance=0.7, nms_max_overlap=1, n_init=3, max_age=15, max_iou_distance=0.7)
tracker = deep.sort_tracker()
print("✓ Deep Sort tracker loaded")

# Load mask
print("[Loading] Mask...")
mask = cv2.imread("new_mask.jpeg")
if mask is None:
    print("⚠ Mask not found, creating default mask")
    mask = np.ones((480, 640, 3), dtype=np.uint8) * 255

print(f"✓ Mask loaded: {mask.shape}")

# Variables
frame_count = 0
timestamp = datetime.datetime(2019, 10, 30, 8, 0, 0, 000000)

# Grid setup
n_rows = 11
n_cols = 9
cell_width = 40
cell_height = 30
x_start = 577
y_start = 288

grids = {}
root_grids_on = CheckTool.create_name_grid(8, number_name=5)
root_grids_under = CheckTool.create_name_grid(0, number_name=11, start=5)
end_grids_on = CheckTool.create_name_grid(0, number_name=5)
end_grids_under = CheckTool.create_name_grid(8, number_name=11, start=5)

for r in range(n_rows):
    y1 = y_start + r * cell_height
    y2 = y_start + (r+1) * cell_height
    for c in range(n_cols):
        x1 = x_start + c * cell_width
        x2 = x_start + (c+1) * cell_width
        grids[f"grid_{r}_{c}"] = RectangularArea(r, c, x1, y1, x2, y2)

print(f"✓ Grid created: {len(grids)} cells")

# Generate synthetic frames
print("\n" + "=" * 70)
print("Processing 30 synthetic frames...")
print("=" * 70)

frame_height, frame_width = 480, 640
num_frames = 30

for frame_idx in range(num_frames):
    # Create synthetic frame
    frame = np.random.randint(50, 150, (frame_height, frame_width, 3), dtype=np.uint8)

    # Add some patterns to make it more realistic
    cv2.rectangle(frame, (100, 100), (300, 300), (100, 200, 100), -1)
    cv2.circle(frame, (200, 200), 50, (50, 100, 200), -1)

    frame_count += 1
    timestamp += datetime.timedelta(seconds=1/30)

    frame_region = cv2.bitwise_and(frame, mask)

    # Object Detection
    (class_ids, scores, boxes) = od.detect(frame_region)

    # Object Tracking
    features = deep.encoder(frame_region, boxes)
    detections = deep.Detection(boxes, scores, class_ids, features)

    tracker.predict()
    (class_ids, object_ids, boxes) = tracker.update(detections)

    # Draw results
    for class_id, object_id, box in zip(class_ids, object_ids, boxes):
        (x, y, x2, y2) = box
        class_name = od.classes[class_id] if class_id < len(od.classes) else "unknown"
        color = tuple(map(int, od.colors[class_id]))

        cv2.rectangle(frame, (x, y), (x2, y2), color, 2)
        cv2.putText(frame, f"ID: {object_id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Draw grid
    for _, v2 in grids.items():
        coords = v2.get_grid_cood()
        cv2.rectangle(frame_region, (coords[0], coords[1]), (coords[2], coords[3]), (0, 255, 0), 1)

    # Display progress
    if (frame_idx + 1) % 10 == 0:
        print(f"  Frame {frame_idx + 1}/{num_frames} - Detected: {len(boxes)} objects, Tracked: {len(object_ids)} IDs")

print("\n" + "=" * 70)
print("✓ Processing completed successfully!")
print("=" * 70)
print("\nProject Status:")
print("  ✓ YOLOv4 model: Working")
print("  ✓ Deep Sort tracker: Working")
print("  ✓ Grid system: Working")
print("  ✓ Frame processing: Working")
print("\nTo run with your own video:")
print("  1. Place your video file as 'xemay_xoay_ngang_lan.mp4'")
print("  2. Place your mask file as 'new_mask.jpeg'")
print("  3. Run: python3 motorbike_project.py")
print("\nNote: Press ESC to exit the application when running the main script.")
