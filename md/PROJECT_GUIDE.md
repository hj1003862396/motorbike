# 摩托车检测项目 - 完整指南

## 📋 项目概述

这是一个基于 YOLOv4 和 Deep Sort 的摩托车检测和跟踪系统。项目能够：
- ✓ 检测视频中的摩托车
- ✓ 为每个摩托车分配唯一 ID
- ✓ 跟踪摩托车的运动轨迹
- ✓ 计算摩托车速度
- ✓ 将摩托车分配到网格区域

## 🚀 快速开始

### 第一步：查看效果（最简单）

直接打开生成的输出视频：
```bash
open /Users/hanjie/PycharmProjects/Motorbike-detection/output_detection.mp4
```

### 第二步：处理你的视频

1. 将你的视频文件放在项目目录中
2. 修改脚本中的视频文件名
3. 运行处理脚本

```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
python3 save_output_video.py
```

## 📁 项目文件说明

### 核心文件

| 文件 | 说明 |
|------|------|
| `motorbike_project.py` | 主项目文件（完整版，需要显示窗口） |
| `save_output_video.py` | **推荐使用** - 处理视频并保存结果 |
| `run_video.py` | 快速处理视频，输出统计数据 |
| `demo_run.py` | 演示版本（使用合成帧） |
| `test_setup.py` | 测试环境是否正确配置 |

### 模块文件

| 文件 | 说明 |
|------|------|
| `object_detection.py` | 对象检测模块（YOLOv4） |
| `deep_sort_wrapper.py` | 对象跟踪模块（Deep Sort） |
| `grid.py` | 网格系统模块 |

### 模型文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `yolov4.weights` | 246 MB | YOLOv4 预训练权重 |
| `yolov4.cfg` | 12 KB | YOLOv4 网络配置 |
| `coco.names` | 625 B | 类别名称文件 |
| `new_mask.jpeg` | 7.7 KB | 掩码图像 |

### 输入/输出文件

| 文件 | 说明 |
|------|------|
| `a.mp4` | 输入视频文件 |
| `output_detection.mp4` | 输出视频（带检测框和 ID） |

## 🎬 使用方法

### 方法 1：生成可视化视频（推荐）

最直观的方式，生成带有检测框和跟踪 ID 的视频：

```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
python3 save_output_video.py
```

**输出：**
- `output_detection.mp4` - 带有检测结果的视频
- 控制台显示处理进度和统计数据

**视频中包含：**
- 绿色检测框 - 标记检测到的对象
- ID 标签 - 每个对象的唯一跟踪 ID
- 类别名称 - 检测到的对象类别
- 网格线 - 99 个网格单元的划分
- 统计信息 - 当前帧的检测和跟踪数量

### 方法 2：快速处理（仅统计数据）

如果只需要统计数据，不需要保存视频：

```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
python3 run_video.py
```

**输出：**
- 处理进度
- 每帧的检测和跟踪数量
- 平均统计数据

### 方法 3：演示版本（合成帧）

使用合成视频帧进行演示，不需要真实视频：

```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
python3 demo_run.py
```

### 方法 4：完整项目（实时显示）

运行完整项目，实时显示检测结果（需要显示窗口）：

```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
python3 motorbike_project.py
```

**按 ESC 键退出**

## 📊 输出结果解释

### 视频输出示例

```
Frame: 5/12
Detections: 2
Tracked IDs: 2
```

- **Frame** - 当前处理的帧号
- **Detections** - 当前帧检测到的对象数
- **Tracked IDs** - 当前帧正在跟踪的对象数

### 统计数据示例

```
Processing Statistics:
  Total frames processed: 12
  Average detections per frame: 1.50
  Average tracked objects per frame: 1.17
  Max detections in a frame: 2
  Max tracked objects in a frame: 2
```

- **Total frames** - 处理的总帧数
- **Average detections** - 平均每帧检测数
- **Average tracked** - 平均每帧跟踪数
- **Max detections** - 单帧最大检测数
- **Max tracked** - 单帧最大跟踪数

## 🎯 处理自己的视频

### 步骤 1：准备视频文件

1. 将你的视频文件放在项目目录中
2. 记住文件名（例如：`my_video.mp4`）

### 步骤 2：修改脚本

编辑 `save_output_video.py`，找到这一行：

```python
cap = cv2.VideoCapture("a.mp4")
```

改为你的视频文件名：

```python
cap = cv2.VideoCapture("my_video.mp4")
```

### 步骤 3：运行脚本

```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
python3 save_output_video.py
```

### 步骤 4：查看结果

```bash
open output_detection.mp4
```

## 📹 视频效果优化建议

### 什么样的视频效果最好？

**✓ 最佳条件：**
- 视频长度：30-60 秒
- 分辨率：720p 或以上
- 帧率：24-30 FPS
- 光线：白天、充足光线
- 内容：多个摩托车，不同速度和方向

**✗ 不理想的条件：**
- 视频太短（< 5 秒）
- 分辨率太低（< 480p）
- 帧率太低（< 15 FPS）
- 光线不足（夜间、逆光）
- 背景复杂（树木、建筑物遮挡）

### 理想场景示例

```
- 摩托车在宽敞的道路上行驶
- 白天、光线充足
- 3-5 辆摩托车
- 不同速度和方向
- 摩托车占画面 5-30%
```

## 🔧 配置参数说明

### YOLOv4 检测参数

在 `save_output_video.py` 中：

```python
od.load_detection_model(
    image_size=416,        # 输入图像大小（416-1280）
    nmsThreshold=0.4,      # NMS 阈值（0-1，越小越严格）
    confThreshold=0.3      # 置信度阈值（0-1，越高越严格）
)
```

- **image_size** - 更大的值更准确但更慢
- **nmsThreshold** - 更小的值减少重复检测
- **confThreshold** - 更高的值减少误检

### Deep Sort 跟踪参数

```python
deep = Deep(
    max_distance=0.7,           # 最大匹配距离
    nms_max_overlap=1,          # NMS 最大重叠
    n_init=3,                   # 初始化帧数
    max_age=15,                 # 最大年龄
    max_iou_distance=0.7        # IOU 距离阈值
)
```

- **max_distance** - 越小跟踪越严格
- **n_init** - 越小越快确认新轨迹
- **max_age** - 越大越容易保持轨迹

## 🐛 故障排除

### 问题 1：找不到视频文件

**错误信息：**
```
Warning: Video file not found. Using webcam instead.
```

**解决方案：**
1. 确保视频文件在项目目录中
2. 检查文件名是否正确
3. 确保文件名与脚本中的一致

### 问题 2：模型加载失败

**错误信息：**
```
Error loading model: ...
```

**解决方案：**
1. 检查 `yolov4.weights` 是否存在（246 MB）
2. 检查 `yolov4.cfg` 是否存在
3. 检查 `coco.names` 是否存在

### 问题 3：网络连接问题

**错误信息：**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**解决方案：**
使用代理设置运行脚本：
```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
python3 save_output_video.py
```

### 问题 4：输出视频无法打开

**解决方案：**
1. 检查输出文件是否存在：`ls -lh output_detection.mp4`
2. 尝试用不同的播放器打开
3. 检查磁盘空间是否充足

## 📈 性能指标

### 当前系统性能

基于 a.mp4 的处理结果：

| 指标 | 值 |
|------|-----|
| 视频分辨率 | 852x572 |
| 帧率 | 13.8 FPS |
| 总帧数 | 12 |
| 平均检测数/帧 | 1.50 |
| 平均跟踪数/帧 | 1.17 |
| 处理时间 | < 1 分钟 |

### 优化建议

- 使用更高质量的视频
- 增加视频长度以获得更多样本
- 调整检测和跟踪参数
- 使用 GPU 加速（如果可用）

## 📚 相关文件

- **原始项目文件** - `motorbike_project.py`
- **网格系统** - `grid.py`
- **README** - `README.md`

## 🔗 依赖项

- Python 3.13+
- OpenCV 4.13+
- NumPy
- SciPy
- scikit-learn

## 💡 常见问题

**Q: 为什么检测数量这么少？**
A: 这取决于视频内容。如果视频中摩托车较少或不清晰，检测数量会较少。

**Q: 如何提高检测准确度？**
A:
1. 使用更清晰的视频
2. 调整 `confThreshold` 参数
3. 使用自定义训练的模型

**Q: 如何加快处理速度？**
A:
1. 减小 `image_size` 参数
2. 使用 GPU 加速
3. 处理较短的视频

**Q: 输出视频的格式是什么？**
A: MP4 格式，可以用任何视频播放器打开。

## 📞 支持

如有问题，请检查：
1. 所有文件是否存在
2. Python 版本是否正确
3. 依赖项是否安装
4. 代理设置是否正确

---

**最后更新：** 2026-01-30
**项目状态：** ✓ 正常运行
