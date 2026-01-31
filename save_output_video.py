#!/usr/bin/env python3
"""
Motorbike Detection Project - Save Output Video
Processes video and saves results with detection boxes and tracking IDs
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
print("Motorbike Detection - Saving Output Video")
print("=" * 70)

# Load Object Detection
print("\n[1/5] Loading YOLOv4 model...")
od = ObjectDetection("yolov4.weights", "yolov4.cfg")
od.load_class_names("coco.names")
od.load_detection_model(image_size=416, nmsThreshold=0.5, confThreshold=0.4)
print("✓ YOLOv4 model loaded")

# Load Object Tracking Deep Sort
print("[2/5] Loading Deep Sort tracker...")
deep = Deep(max_distance=0.75, nms_max_overlap=1, n_init=3, max_age=20, max_iou_distance=0.7)
tracker = deep.sort_tracker()
print("✓ Deep Sort tracker loaded")

# Load mask
print("[3/5] Loading mask...")
mask = cv2.imread("new_mask.jpeg")
if mask is None:
    print("⚠ Mask not found, using full frame")
    mask = None
else:
    print(f"✓ Mask loaded: {mask.shape}")

# Load video
print("[4/5] Loading video...")
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

# Setup video writer
output_path = "output_detection.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

if not out.isOpened():
    print(f"✗ Cannot create output video: {output_path}")
    sys.exit(1)

print(f"✓ Output video will be saved to: {output_path}")

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

print("\n[5/5] Processing video...")
print("=" * 70)

frame_idx = 0
detection_count = 0
tracking_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    frame_idx += 1
    timestamp += datetime.timedelta(seconds=1/fps)

    # Apply mask if available
    if mask is not None:
        mask_resized = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
        frame_region = cv2.bitwise_and(frame, mask_resized)
    else:
        frame_region = frame

    # Object Detection
    (class_ids, scores, boxes) = od.detect(frame_region)

    # Filter only motorcycles (class_id = 3)
    MOTORBIKE_CLASS_ID = 3
    filtered_boxes = []
    filtered_scores = []
    filtered_class_ids = []

    for class_id, score, box in zip(class_ids, scores, boxes):
        if class_id == MOTORBIKE_CLASS_ID:
            filtered_boxes.append(box)
            filtered_scores.append(score)
            filtered_class_ids.append(class_id)

    detection_count += len(filtered_boxes)

    # Object Tracking
    features = deep.encoder(frame_region, filtered_boxes)
    detections = deep.Detection(filtered_boxes, filtered_scores, filtered_class_ids, features)

    tracker.predict()
    (tracked_class_ids, object_ids, tracked_boxes) = tracker.update(detections)
    tracking_count += len(object_ids)

    # Draw detections and tracking on frame
    output_frame = frame.copy()

    # Draw tracked objects
    for class_id, object_id, box in zip(tracked_class_ids, object_ids, tracked_boxes):
        (x, y, x2, y2) = box
        class_name = od.classes[class_id] if class_id < len(od.classes) else "unknown"
        color = tuple(map(int, od.colors[class_id]))

        # Draw bounding box
        cv2.rectangle(output_frame, (x, y), (x2, y2), color, 2)

        # Draw ID
        cv2.putText(output_frame, f"ID: {object_id}", (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Draw class name
        cv2.putText(output_frame, class_name, (x, y2 + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Draw grid
    for _, v2 in grids.items():
        coords = v2.get_grid_cood()
        cv2.rectangle(output_frame, (coords[0], coords[1]), (coords[2], coords[3]),
                     (0, 255, 0), 1)

    # Draw statistics
    cv2.putText(output_frame, f"Frame: {frame_idx}/{total_frames}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(output_frame, f"Detections: {len(boxes)}", (10, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(output_frame, f"Tracked IDs: {len(object_ids)}", (10, 90),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Write frame to output video
    out.write(output_frame)

    # Print progress
    if frame_idx % 5 == 0 or frame_idx == total_frames:
        progress = (frame_idx / total_frames) * 100
        print(f"  Progress: {progress:5.1f}% | Frame {frame_idx}/{total_frames} | Detections: {len(boxes)} | Tracked: {len(object_ids)}")

cap.release()
out.release()

print("\n" + "=" * 70)
print("✓ Video processing completed!")
print("=" * 70)

print(f"\nOutput Video: {output_path}")
print(f"  Total frames: {frame_idx}")
print(f"  Total detections: {detection_count}")
print(f"  Total tracked objects: {tracking_count}")
print(f"  Average detections/frame: {detection_count/frame_idx:.2f}")
print(f"  Average tracked/frame: {tracking_count/frame_idx:.2f}")

print("\n📹 You can now view the output video:")
print(f"  open {output_path}")
print("\nOr use any video player to open the file.")
