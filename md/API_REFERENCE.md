# API 参考文档

## ObjectDetection 类

### 初始化

```python
from object_detection import ObjectDetection

od = ObjectDetection(weights_path, config_path)
```

**参数：**
- `weights_path` (str): YOLOv4 权重文件路径
- `config_path` (str): YOLOv4 配置文件路径

**示例：**
```python
od = ObjectDetection("yolov4.weights", "yolov4.cfg")
```

---

### load_class_names()

加载类别名称文件

```python
od.load_class_names(class_names_path)
```

**参数：**
- `class_names_path` (str): 类别名称文件路径

**示例：**
```python
od.load_class_names("coco.names")
```

**文件格式：**
```
person
bicycle
car
motorbike
...
```

---

### load_detection_model()

加载检测模型

```python
od.load_detection_model(image_size=416, nmsThreshold=0.4, confThreshold=0.3)
```

**参数：**
- `image_size` (int): 输入图像大小，范围 416-1280，默认 416
- `nmsThreshold` (float): NMS 阈值，范围 0-1，默认 0.4
- `confThreshold` (float): 置信度阈值，范围 0-1，默认 0.3

**说明：**
- `image_size` 越大越准确但越慢
- `nmsThreshold` 越小越严格，减少重复检测
- `confThreshold` 越高越严格，减少误检

**示例：**
```python
# 高精度
od.load_detection_model(image_size=832, confThreshold=0.5)

# 高速度
od.load_detection_model(image_size=416, confThreshold=0.2)
```

---

### detect()

检测图像中的对象

```python
class_ids, scores, boxes = od.detect(frame)
```

**参数：**
- `frame` (numpy.ndarray): 输入图像，形状 (height, width, 3)

**返回值：**
- `class_ids` (list): 类别 ID 列表
- `scores` (list): 置信度分数列表
- `boxes` (list): 边界框列表，格式 [x, y, w, h]

**示例：**
```python
import cv2
frame = cv2.imread("image.jpg")
class_ids, scores, boxes = od.detect(frame)

for class_id, score, box in zip(class_ids, scores, boxes):
    x, y, w, h = box
    print(f"Class: {od.classes[class_id]}, Score: {score:.2f}")
    print(f"Box: ({x}, {y}, {w}, {h})")
```

---

## Deep 类

### 初始化

```python
from deep_sort_wrapper import Deep

deep = Deep(max_distance=0.7, nms_max_overlap=1, n_init=3, max_age=15, max_iou_distance=0.7)
```

**参数：**
- `max_distance` (float): 最大匹配距离，默认 0.7
- `nms_max_overlap` (float): NMS 最大重叠，默认 1
- `n_init` (int): 初始化帧数，默认 3
- `max_age` (int): 最大年龄，默认 15
- `max_iou_distance` (float): IOU 距离阈值，默认 0.7

---

### sort_tracker()

创建跟踪器

```python
tracker = deep.sort_tracker()
```

**返回值：**
- `tracker` (TrackerWrapper): 跟踪器对象

**示例：**
```python
deep = Deep()
tracker = deep.sort_tracker()
```

---

### encoder()

提取特征向量

```python
features = deep.encoder(frame, boxes)
```

**参数：**
- `frame` (numpy.ndarray): 输入图像
- `boxes` (list): 边界框列表

**返回值：**
- `features` (numpy.ndarray): 特征向量，形状 (n_boxes, 128)

**示例：**
```python
features = deep.encoder(frame, boxes)
print(f"Features shape: {features.shape}")
```

---

### Detection()

创建检测对象

```python
detections = deep.Detection(boxes, scores, class_ids, features)
```

**参数：**
- `boxes` (list): 边界框列表
- `scores` (list): 置信度分数列表
- `class_ids` (list): 类别 ID 列表
- `features` (numpy.ndarray): 特征向量

**返回值：**
- `detections` (list): Detection 对象列表

**示例：**
```python
detections = deep.Detection(boxes, scores, class_ids, features)
```

---

### tracker.predict()

预测轨迹

```python
tracker.predict()
```

**说明：**
- 应该在每一帧之前调用
- 预测轨迹的下一个位置

**示例：**
```python
tracker.predict()
```

---

### tracker.update()

更新跟踪器

```python
class_ids, object_ids, boxes = tracker.update(detections)
```

**参数：**
- `detections` (list): Detection 对象列表

**返回值：**
- `class_ids` (list): 类别 ID 列表
- `object_ids` (list): 跟踪 ID 列表
- `boxes` (list): 边界框列表，格式 [x1, y1, x2, y2]

**示例：**
```python
class_ids, object_ids, boxes = tracker.update(detections)

for class_id, object_id, box in zip(class_ids, object_ids, boxes):
    x1, y1, x2, y2 = box
    print(f"ID: {object_id}, Box: ({x1}, {y1}, {x2}, {y2})")
```

---

## RectangularArea 类

### 初始化

```python
from grid import RectangularArea

grid = RectangularArea(row, col, x1, y1, x2, y2)
```

**参数：**
- `row` (int): 网格行号
- `col` (int): 网格列号
- `x1, y1` (int): 左上角坐标
- `x2, y2` (int): 右下角坐标

**示例：**
```python
grid = RectangularArea(0, 0, 100, 100, 200, 200)
```

---

### contains()

检查点是否在网格内

```python
is_inside = grid.contains(x, y)
```

**参数：**
- `x, y` (int): 点的坐标

**返回值：**
- `is_inside` (bool): 是否在网格内

**示例：**
```python
if grid.contains(150, 150):
    print("Point is inside the grid")
```

---

### add_object()

添加对象到网格

```python
grid.add_object(object_id, frame_count, timestamp, position)
```

**参数：**
- `object_id` (int): 对象 ID
- `frame_count` (int): 帧号
- `timestamp` (datetime): 时间戳
- `position` (list): 位置 [x, y]

**示例：**
```python
import datetime
grid.add_object(1, 100, datetime.datetime.now(), [150, 150])
```

---

### check_object()

检查对象是否在网格中

```python
exists = grid.check_object(object_id)
```

**参数：**
- `object_id` (int): 对象 ID

**返回值：**
- `exists` (bool): 对象是否存在

**示例：**
```python
if grid.check_object(1):
    print("Object 1 is in this grid")
```

---

### calculate_instant_speed()

计算瞬时速度

```python
grid.calculate_instant_speed(object_id, grids, root_grids)
```

**参数：**
- `object_id` (int): 对象 ID
- `grids` (dict): 所有网格字典
- `root_grids` (list): 根网格列表

**示例：**
```python
grid.calculate_instant_speed(1, grids, root_grids_on + root_grids_under)
```

---

### calculate_spatial_speed()

计算空间速度

```python
grid.calculate_spatial_speed(object_id, root_grids, grids)
```

**参数：**
- `object_id` (int): 对象 ID
- `root_grids` (list): 根网格列表
- `grids` (dict): 所有网格字典

**示例：**
```python
grid.calculate_spatial_speed(1, root_grids_on + root_grids_under, grids)
```

---

## CheckTool 类

### create_name_grid()

创建网格名称列表

```python
from grid import CheckTool

grid_names = CheckTool.create_name_grid(start_row, number_name, start=0)
```

**参数：**
- `start_row` (int): 起始行号
- `number_name` (int): 网格数量
- `start` (int): 起始列号，默认 0

**返回值：**
- `grid_names` (list): 网格名称列表

**示例：**
```python
# 创建第 0 行的 5 个网格
grids = CheckTool.create_name_grid(0, 5)
# 返回: ['grid_0_0', 'grid_0_1', 'grid_0_2', 'grid_0_3', 'grid_0_4']

# 创建第 8 行的 11 个网格，从列 5 开始
grids = CheckTool.create_name_grid(8, 11, start=5)
# 返回: ['grid_8_5', 'grid_8_6', ..., 'grid_8_15']
```

---

## 完整使用示例

### 基础检测和跟踪

```python
import cv2
from object_detection import ObjectDetection
from deep_sort_wrapper import Deep

# 初始化
od = ObjectDetection("../yolov4.weights", "yolov4.cfg")
od.load_class_names("coco.names")
od.load_detection_model(image_size=416, nmsThreshold=0.4, confThreshold=0.3)

deep = Deep()
tracker = deep.sort_tracker()

# 打开视频
cap = cv2.VideoCapture("video.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 检测
    class_ids, scores, boxes = od.detect(frame)

    # 跟踪
    features = deep.encoder(frame, boxes)
    detections = deep.Detection(boxes, scores, class_ids, features)
    tracker.predict()
    tracked_class_ids, object_ids, tracked_boxes = tracker.update(detections)

    # 绘制结果
    for class_id, object_id, box in zip(tracked_class_ids, object_ids, tracked_boxes):
        x1, y1, x2, y2 = box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {object_id}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
```

---

**最后更新：** 2026-01-30
