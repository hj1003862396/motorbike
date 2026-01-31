# 安装和配置指南

## 📦 系统要求

- **操作系统**：macOS 10.14+
- **Python**：3.9 或更高版本
- **磁盘空间**：至少 500 MB（包括模型文件）
- **内存**：4 GB 或更多
- **网络**：需要代理访问 PyPI（可选）

## 🔧 安装步骤

### 步骤 1：检查 Python 版本

```bash
python3 --version
```

应该显示 Python 3.9 或更高版本。

### 步骤 2：安装依赖

使用代理设置安装依赖：

```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890

python3 -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org \
  opencv-python \
  numpy \
  scipy \
  scikit-learn \
  pandas \
  sqlalchemy \
  psycopg2-binary
```

### 步骤 3：验证安装

```bash
python3 -c "import cv2, numpy, scipy; print('✓ All dependencies installed')"
```

### 步骤 4：下载模型文件

模型文件已经下载到项目目录：
- `yolov4.weights` (246 MB)
- `yolov4.cfg` (12 KB)
- `coco.names` (625 B)

如果缺少，可以手动下载：

```bash
# 下载权重文件
curl -L -o yolov4.weights https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

# 下载配置文件
curl -o yolov4.cfg https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg

# 下载类别文件
curl -o coco.names https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names
```

### 步骤 5：验证项目

```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
python3 test_setup.py
```

应该看到所有测试都通过。

## 🌐 代理配置

如果你在中国或需要代理访问，使用以下命令：

```bash
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890
```

然后运行任何 Python 脚本。

### 永久配置（可选）

编辑 `~/.zshrc` 或 `~/.bash_profile`，添加：

```bash
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890
```

然后运行：
```bash
source ~/.zshrc  # 或 source ~/.bash_profile
```

## 📋 依赖项详解

| 包 | 版本 | 用途 |
|-----|------|------|
| opencv-python | 4.13+ | 视频处理和图像操作 |
| numpy | 1.26+ | 数值计算 |
| scipy | 1.13+ | 科学计算（Deep Sort 需要） |
| scikit-learn | 1.3+ | 机器学习工具 |
| pandas | 2.0+ | 数据处理 |
| sqlalchemy | 2.0+ | 数据库 ORM |
| psycopg2-binary | 2.9+ | PostgreSQL 驱动 |

## ✅ 验证安装

运行以下命令验证所有组件：

```bash
python3 << 'EOF'
import cv2
import numpy as np
import scipy
import sklearn
print("✓ OpenCV:", cv2.__version__)
print("✓ NumPy:", np.__version__)
print("✓ SciPy:", scipy.__version__)
print("✓ scikit-learn:", sklearn.__version__)
print("\n✓ All dependencies installed successfully!")
EOF
```

## 🚀 首次运行

第一次运行时，系统会：
1. 加载 YOLOv4 模型（可能需要 10-30 秒）
2. 初始化 Deep Sort 跟踪器
3. 处理视频帧

这是正常的，后续运行会更快。

## 🔄 更新依赖

如果需要更新依赖：

```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890

python3 -m pip install --upgrade \
  opencv-python \
  numpy \
  scipy \
  scikit-learn
```

## 🐛 常见安装问题

### 问题 1：SSL 证书错误

**错误信息：**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**解决方案：**
使用代理设置或 `--trusted-host` 标志：

```bash
python3 -m pip install --trusted-host pypi.org opencv-python
```

### 问题 2：找不到 Python 模块

**错误信息：**
```
ModuleNotFoundError: No module named 'cv2'
```

**解决方案：**
确保使用正确的 Python 版本：

```bash
which python3
python3 -m pip list | grep opencv
```

### 问题 3：权限错误

**错误信息：**
```
Permission denied
```

**解决方案：**
使用 `--user` 标志：

```bash
python3 -m pip install --user opencv-python
```

### 问题 4：磁盘空间不足

**错误信息：**
```
No space left on device
```

**解决方案：**
检查磁盘空间：

```bash
df -h
```

清理不需要的文件，或使用外部存储。

## 📊 系统信息

查看你的系统信息：

```bash
python3 << 'EOF'
import platform
import sys
print("Python Version:", sys.version)
print("Platform:", platform.platform())
print("Processor:", platform.processor())
EOF
```

## 🔗 相关资源

- [OpenCV 官网](https://opencv.org/)
- [YOLOv4 GitHub](https://github.com/AlexeyAB/darknet)
- [Deep Sort GitHub](https://github.com/nwojke/deep_sort)
- [NumPy 文档](https://numpy.org/)

## 💾 备份和恢复

### 备份项目

```bash
tar -czf motorbike-detection-backup.tar.gz /Users/hanjie/PycharmProjects/Motorbike-detection/
```

### 恢复项目

```bash
tar -xzf motorbike-detection-backup.tar.gz
```

## 🔐 安全建议

- 不要在代码中硬编码敏感信息
- 使用环境变量存储配置
- 定期更新依赖项
- 备份重要的输出文件

---

**最后更新：** 2026-01-30
