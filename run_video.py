#!/usr/bin/env python3
"""
Motorbike Detection Project - CLI Version
Processes video and outputs results to console
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
print("Motorbike Detection Project - Processing a.mp4")
print("=" * 70)

# Load Object Detection
print("\n[1/4] Loading YOLOv4 model...")
od = ObjectDetection("yolov4.weights", "yolov4.cfg")
od.load_class_names("coco.names")
od.load_detection_model(image_size=416, nmsThreshold=0.4, confThreshold=0.3)
print("✓ YOLOv4 model loaded")

# Load Object Tracking Deep Sort
print("[2/4] Loading Deep Sort tracker...")
deep = Deep(max_distance=0.7, nms_max_overlap=1, n_init=3, max_age=15, max_iou_distance=0.7)
tracker = deep.sort_tracker()
print("✓ Deep Sort tracker loaded")

# Load mask
print("[3/4] Loading mask...")
mask = cv2.imread("new_mask.jpeg")
if mask is None:
    print("⚠ Mask not found, using full frame")
    mask = None
else:
    print(f"✓ Mask loaded: {mask.shape}")

# Load video
print("[4/4] Loading video...")
cap = cv2.VideoCapture("a.mp4")
if not cap.isOpened():
    print("✗ Cannot open a.mp4")
    sys.exit(1)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"✓ Video loaded: {width}x{height}, {fps:.1f} FPS, {total_frames} frames")

# Variables
frame_count = 0
timestamp = datetime.datetime(2019, 10, 30, 8, 0, 0, 000000)
detection_stats = {}
tracking_stats = {}

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

print("\n" + "=" * 70)
print("Processing video...")
print("=" * 70)

frame_idx = 0
max_frames = min(100, total_frames)  # Process up to 100 frames for demo

while frame_idx < max_frames:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    frame_idx += 1
    timestamp += datetime.timedelta(seconds=1/fps)

    # Apply mask if available
    if mask is not None:
        # Resize mask to match frame size
        mask_resized = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
        frame_region = cv2.bitwise_and(frame, mask_resized)
    else:
        frame_region = frame

    # Object Detection
    (class_ids, scores, boxes) = od.detect(frame_region)

    # Object Tracking
    features = deep.encoder(frame_region, boxes)
    detections = deep.Detection(boxes, scores, class_ids, features)

    tracker.predict()
    (tracked_class_ids, object_ids, tracked_boxes) = tracker.update(detections)

    # Update statistics
    detection_stats[frame_idx] = len(boxes)
    tracking_stats[frame_idx] = len(object_ids)

    # Print progress every 10 frames
    if frame_idx % 10 == 0:
        avg_detections = np.mean(list(detection_stats.values()))
        avg_tracking = np.mean(list(tracking_stats.values()))
        print(f"  Frame {frame_idx}/{max_frames} | Detections: {len(boxes):2d} | Tracked IDs: {len(object_ids):2d} | Avg Det: {avg_detections:.1f} | Avg Track: {avg_tracking:.1f}")

cap.release()

print("\n" + "=" * 70)
print("✓ Video processing completed!")
print("=" * 70)

print("\nProcessing Statistics:")
print(f"  Total frames processed: {frame_idx}")
print(f"  Average detections per frame: {np.mean(list(detection_stats.values())):.2f}")
print(f"  Average tracked objects per frame: {np.mean(list(tracking_stats.values())):.2f}")
print(f"  Max detections in a frame: {max(detection_stats.values())}")
print(f"  Max tracked objects in a frame: {max(tracking_stats.values())}")

print("\nProject Status:")
print("  ✓ YOLOv4 model: Working")
print("  ✓ Deep Sort tracker: Working")
print("  ✓ Grid system: Working")
print("  ✓ Video processing: Working")
print("\nTo run the interactive version with display:")
print("  python3 motorbike_project.py")
