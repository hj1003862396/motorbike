import numpy as np
from deep_sort.deep_sort import tracker as tracker_module
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort import detection as detection_module

class TrackerWrapper:
    """Wrapper around deep_sort Tracker to provide compatible interface"""
    def __init__(self, tracker):
        self.tracker = tracker
        self.last_class_ids = {}  # Store class_id for each track_id

    def predict(self):
        self.tracker.predict()

    def update(self, detections):
        """Update tracker and return results in compatible format"""
        self.tracker.update(detections)

        # Extract confirmed tracks
        class_ids = []
        object_ids = []
        boxes = []

        for track in self.tracker.tracks:
            if not track.is_confirmed():
                continue

            # Get bounding box in [x1, y1, x2, y2] format
            tlwh = track.to_tlwh()
            x, y, w, h = tlwh
            x2 = x + w
            y2 = y + h

            boxes.append([int(x), int(y), int(x2), int(y2)])
            object_ids.append(track.track_id)

            # Use stored class_id or default to 0
            class_id = self.last_class_ids.get(track.track_id, 0)
            class_ids.append(class_id)

        return (class_ids, object_ids, boxes)

    def store_class_ids(self, object_ids, class_ids):
        """Store class_ids for tracks"""
        for obj_id, class_id in zip(object_ids, class_ids):
            self.last_class_ids[obj_id] = class_id

class Deep:
    def __init__(self, max_distance=0.7, nms_max_overlap=1, n_init=3, max_age=15, max_iou_distance=0.7):
        self.max_distance = max_distance
        self.nms_max_overlap = nms_max_overlap
        self.n_init = n_init
        self.max_age = max_age
        self.max_iou_distance = max_iou_distance
        self.tracker = None
        self.metric = None
        self.wrapper = None

    def sort_tracker(self):
        # Create distance metric
        self.metric = nn_matching.NearestNeighborDistanceMetric(
            "cosine", self.max_distance, None
        )
        # Create tracker
        base_tracker = tracker_module.Tracker(
            self.metric,
            max_iou_distance=self.max_iou_distance,
            max_age=self.max_age,
            n_init=self.n_init
        )
        self.wrapper = TrackerWrapper(base_tracker)
        self.tracker = self.wrapper
        return self.tracker

    def encoder(self, frame, boxes):
        """
        Simple feature encoder - returns dummy features for now
        In a real implementation, this would use a CNN to extract features
        """
        features = []
        for box in boxes:
            # Create a dummy feature vector (128-dim)
            feature = np.random.randn(128)
            feature = feature / np.linalg.norm(feature)
            features.append(feature)
        return np.array(features)

    def Detection(self, boxes, scores, class_ids, features):
        """
        Create Detection objects for the tracker
        """
        detections = []
        for box, score, class_id, feature in zip(boxes, scores, class_ids, features):
            x, y, w, h = box
            # Convert to [x1, y1, x2, y2] format
            detection = detection_module.Detection(
                tlwh=np.array([x, y, w, h]),
                confidence=score,
                feature=feature
            )
            detections.append(detection)
        return detections
