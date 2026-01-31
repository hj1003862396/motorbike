# 故障排除指南

## 🔍 常见问题和解决方案

### 1. 模型加载问题

#### 问题：找不到模型文件

**错误信息：**
```
FileNotFoundError: [Errno 2] No such file or directory: 'yolov4.weights'
```

**原因：**
- 模型文件不在项目目录中
- 文件名拼写错误
- 文件被移动或删除

**解决方案：**

1. 检查文件是否存在：
```bash
ls -lh yolov4.weights yolov4.cfg coco.names
```

2. 如果文件缺失，重新下载：
```bash
curl -L -o yolov4.weights https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
curl -o yolov4.cfg https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg
curl -o coco.names https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names
```

3. 检查文件大小：
```bash
# yolov4.weights 应该是 ~246 MB
# yolov4.cfg 应该是 ~12 KB
# coco.names 应该是 ~625 B
```

---

#### 问题：模型加载很慢

**原因：**
- 第一次加载需要初始化
- 磁盘 I/O 缓慢
- 系统资源不足

**解决方案：**

1. 这是正常的，第一次加载可能需要 10-30 秒
2. 后续运行会更快（使用缓存）
3. 确保有足够的内存：
```bash
# 检查可用内存
free -h  # Linux
vm_stat  # macOS
```

---

### 2. 视频处理问题

#### 问题：找不到视频文件

**错误信息：**
```
Warning: Video file not found. Using webcam instead.
```

**原因：**
- 视频文件不在项目目录
- 文件名拼写错误
- 文件格式不支持

**解决方案：**

1. 检查文件是否存在：
```bash
ls -lh a.mp4
```

2. 检查文件格式：
```bash
file a.mp4
```

3. 确保文件名与脚本中的一致：
```python
# 在 save_output_video.py 中检查
cap = cv2.VideoCapture("a.mp4")  # 确保这里的文件名正确
```

4. 支持的格式：MP4, AVI, MOV, MKV 等

---

#### 问题：视频无法读取

**错误信息：**
```
OpenCV: Couldn't read video stream from file
```

**原因：**
- 视频文件损坏
- 编码格式不支持
- 文件权限问题

**解决方案：**

1. 检查文件是否完整：
```bash
# 使用 ffprobe 检查
ffprobe a.mp4
```

2. 转换视频格式：
```bash
# 使用 ffmpeg 转换为 MP4
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4
```

3. 检查文件权限：
```bash
chmod 644 a.mp4
```

---

#### 问题：掩码尺寸不匹配

**错误信息：**
```
cv2.error: (-209:Sizes of input arguments do not match)
```

**原因：**
- 掩码和视频分辨率不同

**解决方案：**

这个问题已经在代码中修复了。如果仍然出现，检查：

```python
# 确保掩码被正确调整大小
if mask is not None:
    mask_resized = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
    frame_region = cv2.bitwise_and(frame, mask_resized)
```

---

### 3. 依赖项问题

#### 问题：模块导入失败

**错误信息：**
```
ModuleNotFoundError: No module named 'cv2'
```

**原因：**
- 依赖项未安装
- 使用了错误的 Python 版本

**解决方案：**

1. 检查 Python 版本：
```bash
python3 --version
```

2. 安装缺失的依赖：
```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890

python3 -m pip install opencv-python numpy scipy scikit-learn
```

3. 验证安装：
```bash
python3 -c "import cv2, numpy, scipy; print('OK')"
```

---

#### 问题：版本冲突

**错误信息：**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
```

**原因：**
- 不同包之间的版本不兼容

**解决方案：**

1. 升级 pip：
```bash
python3 -m pip install --upgrade pip
```

2. 重新安装依赖：
```bash
python3 -m pip install --upgrade --force-reinstall opencv-python numpy scipy
```

---

### 4. 网络问题

#### 问题：SSL 证书错误

**错误信息：**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**原因：**
- SSL 证书验证失败
- 网络连接问题

**解决方案：**

1. 使用代理设置：
```bash
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890
```

2. 使用 `--trusted-host` 标志：
```bash
python3 -m pip install --trusted-host pypi.org opencv-python
```

3. 禁用 SSL 验证（不推荐）：
```bash
python3 -m pip install --index-url http://pypi.python.org/simple/ opencv-python
```

---

### 5. 输出问题

#### 问题：输出视频无法打开

**错误信息：**
```
Cannot open output_detection.mp4
```

**原因：**
- 视频编码失败
- 磁盘空间不足
- 文件权限问题

**解决方案：**

1. 检查文件是否存在：
```bash
ls -lh output_detection.mp4
```

2. 检查磁盘空间：
```bash
df -h
```

3. 尝试用不同的播放器打开
4. 检查文件是否完整：
```bash
ffprobe output_detection.mp4
```

---

#### 问题：输出视频很大

**原因：**
- 视频分辨率高
- 编码质量高
- 视频长度长

**解决方案：**

1. 压缩输出视频：
```bash
ffmpeg -i output_detection.mp4 -c:v libx264 -crf 28 output_compressed.mp4
```

2. 降低输入分辨率
3. 处理较短的视频

---

### 6. 性能问题

#### 问题：处理速度很慢

**原因：**
- 图像大小太大
- 系统资源不足
- 没有 GPU 加速

**解决方案：**

1. 减小图像大小：
```python
od.load_detection_model(image_size=416)  # 改为 416 而不是 832
```

2. 检查系统资源：
```bash
# macOS
top -l 1 | head -20

# Linux
htop
```

3. 关闭其他应用程序
4. 使用 GPU（如果可用）

---

#### 问题：内存不足

**错误信息：**
```
MemoryError
```

**原因：**
- 视频太长
- 系统内存不足

**解决方案：**

1. 处理较短的视频
2. 增加系统内存
3. 关闭其他应用程序

---

### 7. 检测问题

#### 问题：检测数量很少

**原因：**
- 视频中对象较少
- 置信度阈值太高
- 对象太小或不清晰

**解决方案：**

1. 降低置信度阈值：
```python
od.load_detection_model(confThreshold=0.2)  # 改为 0.2 而不是 0.3
```

2. 增加图像大小：
```python
od.load_detection_model(image_size=832)
```

3. 使用更清晰的视频

---

#### 问题：误检太多

**原因：**
- 置信度阈值太低
- 背景复杂

**解决方案：**

1. 提高置信度阈值：
```python
od.load_detection_model(confThreshold=0.5)
```

2. 增加 NMS 阈值：
```python
od.load_detection_model(nmsThreshold=0.5)
```

---

### 8. 跟踪问题

#### 问题：ID 频繁变化

**原因：**
- 跟踪参数不合适
- 对象运动太快

**解决方案：**

1. 调整跟踪参数：
```python
deep = Deep(
    max_distance=0.5,  # 改小以更严格
    max_age=20         # 改大以保持轨迹更久
)
```

2. 增加视频帧率

---

#### 问题：跟踪丢失

**原因：**
- 对象被遮挡
- 对象运动太快
- 跟踪参数不合适

**解决方案：**

1. 调整跟踪参数：
```python
deep = Deep(
    max_distance=0.9,  # 改大以更宽松
    max_age=30         # 改大以保持轨迹更久
)
```

2. 使用更高的帧率视频

---

## 📋 调试检查清单

在报告问题前，请检查：

- [ ] Python 版本是否正确（3.9+）
- [ ] 所有依赖项是否安装
- [ ] 模型文件是否存在且完整
- [ ] 视频文件是否存在且可读
- [ ] 磁盘空间是否充足
- [ ] 内存是否充足
- [ ] 网络连接是否正常
- [ ] 代理设置是否正确

---

## 🔧 诊断脚本

运行以下脚本进行诊断：

```python
import sys
import os
import cv2
import numpy as np

print("=" * 60)
print("System Diagnostics")
print("=" * 60)

# Python 版本
print(f"\nPython Version: {sys.version}")

# 依赖项
print("\nDependencies:")
try:
    import cv2
    print(f"  ✓ OpenCV: {cv2.__version__}")
except:
    print("  ✗ OpenCV: NOT INSTALLED")

try:
    import numpy
    print(f"  ✓ NumPy: {numpy.__version__}")
except:
    print("  ✗ NumPy: NOT INSTALLED")

try:
    import scipy
    print(f"  ✓ SciPy: {scipy.__version__}")
except:
    print("  ✗ SciPy: NOT INSTALLED")

# 文件检查
print("\nFiles:")
files = ['yolov4.weights', 'yolov4.cfg', 'coco.names', 'a.mp4']
for f in files:
    if os.path.exists(f):
        size = os.path.getsize(f) / (1024*1024)
        print(f"  ✓ {f}: {size:.1f} MB")
    else:
        print(f"  ✗ {f}: NOT FOUND")

# 磁盘空间
print("\nDisk Space:")
import shutil
total, used, free = shutil.disk_usage("/")
print(f"  Total: {total / (1024**3):.1f} GB")
print(f"  Used: {used / (1024**3):.1f} GB")
print(f"  Free: {free / (1024**3):.1f} GB")

print("\n" + "=" * 60)
```

---

**最后更新：** 2026-01-30
