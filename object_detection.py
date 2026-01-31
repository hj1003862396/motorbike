import cv2
import numpy as np

class ObjectDetection:
    def __init__(self, weights_path, config_path):
        self.weights_path = weights_path
        self.config_path = config_path
        self.net = None
        self.classes = []
        self.colors = []
        self.output_layers = []

    def load_class_names(self, class_names_path):
        with open(class_names_path, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        # Generate random colors for each class
        np.random.seed(42)
        self.colors = np.random.randint(0, 255, size=(len(self.classes), 3))

    def load_detection_model(self, image_size=416, nmsThreshold=0.4, confThreshold=0.3):
        self.net = cv2.dnn.readNet(self.weights_path, self.config_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        self.image_size = image_size
        self.nmsThreshold = nmsThreshold
        self.confThreshold = confThreshold

        # Get output layer names
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect(self, frame):
        height, width, channels = frame.shape

        # Prepare blob
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (self.image_size, self.image_size),
                                      swapRB=True, crop=False)
        self.net.setInput(blob)

        # Forward pass
        outs = self.net.forward(self.output_layers)

        class_ids = []
        scores = []
        boxes = []

        for out in outs:
            for detection in out:
                scores_list = detection[5:]
                class_id = np.argmax(scores_list)
                confidence = scores_list[class_id]

                if confidence > self.confThreshold:
                    # Get box coordinates
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = center_x - w // 2
                    y = center_y - h // 2

                    boxes.append([x, y, w, h])
                    scores.append(float(confidence))
                    class_ids.append(class_id)

        # Apply NMS
        indices = cv2.dnn.NMSBoxes(boxes, scores, self.confThreshold, self.nmsThreshold)

        final_boxes = []
        final_scores = []
        final_class_ids = []

        if len(indices) > 0:
            for i in indices.flatten():
                final_boxes.append(boxes[i])
                final_scores.append(scores[i])
                final_class_ids.append(class_ids[i])

        return (final_class_ids, final_scores, final_boxes)
