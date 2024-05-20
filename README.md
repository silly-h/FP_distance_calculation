# distance.py 使用说明

`distance.py` 是一个 Python 脚本，用于计算两个 GPS 坐标之间的距离。它使用了多线程和 socket 编程，可以实时读取和处理 GPS 数据。

## 功能

- 自动和手动计算两个 GPS 坐标之间的距离
- 通过按键来控制程序的运行
- 通过 socket 从服务器读取 GPS 数据，并将计算结果发送到另一个服务器

## 使用方法

1. 确保你的 Python 环境已经安装了 `geographiclib` 和 `pynput` 这两个库。如果没有，可以通过 pip 安装：

```bash
pip3 install geographiclib pynput
```

2. 运行 `distance.py` 脚本：

```bash
python3 distance.py
```

3. 在运行脚本后，你可以通过按键来控制程序的运行：

- 按 'a' 键，程序会自动计算距离
- 按 'q' 键，程序会停止自动计算距离
- 按 's' 键，程序会手动计算距离
- 按 'w' 键，程序会停止手动计算距离

## 注意事项

- 请确保TCP信息接收端程序先行启动，否则程序无法运行，示例程序见receive.py
- 请确保你的服务器 IP 和端口设置正确，否则程序可能无法正常运行
- 请确保你的 GPS 数据格式正确，否则程序可能无法正常计算距离

## 依赖

- Python 3
- geographiclib
- pynput

## 输出协议

- 手动：$FP,Manual, gps_week, gps_tow, distance, 记录终止点lat, 记录终止点lon, 记录终止点height, 记录起始点lat, 记录起始点lon, 记录起始点height
    示例：$FP, Manual, 2315, 100686.9, 254.48662114965956, 29.567 476545,106.470110427, 158.3273,29.56906212,106.468269119,159.3005
- 自动：$FP,Auto，gps_week, gps_tow, distance, 记录终止点lat, 记录终止点lon, 记录终止点height, 记录起始点lat, 记录起始点lon, 记录起始点height
    示例：$FP, Auto, 2315, 100686.9, 254.48662114965956, 29.567 476545,106.470110427, 158.3273,29.56906212,106.468269119,159.3005


# distance.py User Guide

`distance.py` is a Python script for calculating the distance between two GPS coordinates. It uses multithreading and socket programming to read and process GPS data in real time.

## Features

- Automatic and manual calculation of the distance between two GPS coordinates
- Control the program operation through key presses
- Read GPS data from a server via socket and send the calculation results to another server

## Usage

1. Ensure that your Python environment has installed the `geographiclib` and `pynput` libraries. If not, you can install them via pip:

```bash
pip3 install geographiclib pynput
```

2. Run the `distance.py` script:

```bash
python3 distance.py
```

3. After running the script, you can control the program operation through key presses:

- Press 'a' to start automatic distance calculation
- Press 'q' to stop automatic distance calculation
- Press 's' to start manual distance calculation
- Press 'w' to stop manual distance calculation

## Precautions

- Please ensure that the TCP information receiving program is started first, otherwise the program cannot run. See `receive.py` for an example program.
- Please ensure that your server IP and port settings are correct, otherwise the program may not run properly
- Please ensure that your GPS data format is correct, otherwise the program may not calculate the distance correctly

## Dependencies

- Python 3
- geographiclib
- pynput

## Output Protocol

- Manual: $FP,Manual, gps_week, gps_tow, distance, record end point lat, record end point lon, record end point height, record start point lat, record start point lon, record start point height
    Example: $FP, Manual, 2315, 100686.9, 254.48662114965956, 29.567 476545,106.470110427, 158.3273,29.56906212,106.468269119,159.3005
- Automatic: $FP,Auto，gps_week, gps_tow, distance, record end point lat, record end point lon, record end point height, record start point lat, record start point lon, record start point height
    Example: $FP, Auto, 2315, 100686.9, 254.48662114965956, 29.567 476545,106.470110427, 158.3273,29.56906212,106.468269119,159.3005
```
