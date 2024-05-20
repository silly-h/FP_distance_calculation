import socket
from geographiclib.geodesic import Geodesic
from collections import deque
import math
from pynput.keyboard import Key, Listener
import threading

# 创建对象和存储数据容器
cond = threading.Condition()
data = {}

# 两个变量来跟踪'a'和's'键是否被按下
a_pressed = False # 自动计算距离，根据GPS状态
s_pressed = False # 手动计算距离


def on_press(key):
    global a_pressed, s_pressed
    key = str(key).replace("'", "")

    if key == 'a' and not a_pressed:
        print('Key "a" is pressed')
        print("\033[35m\nAutomatic calculating distance running...\033[0m")
        a_pressed = True
    elif key == 's' and not s_pressed:
        print('Key "s" is pressed')
        print("\033[35m\nManually calculating distance running...\033[0m")
        s_pressed = True
    elif key == 'q' and a_pressed:
        print('Key "q" is pressed')
        print("\033[35m\nAutomatic calculating distance stoped...\033[0m")
        a_pressed = False
    elif key == 'w' and s_pressed:
        print('Key "w" is pressed')
        print("\033[35m\nManually calculating distance stoped...\033[0m")
        s_pressed = False

def check_key():
    with Listener(on_press=on_press) as listener:
        listener.join()

def calculate_distance(lat1, lon1, alt1, lat2, lon2, alt2):
    geod = Geodesic.WGS84
    g = geod.Inverse(lat1, lon1, lat2, lon2)
    surface_distance = g['s12']
    height_difference = alt2 - alt1
    distance = math.sqrt(surface_distance**2 + height_difference**2)
    return distance

def read_from_socket():
    # 创建并启动检测键盘的线程
    thread = threading.Thread(target=check_key)
    thread.start()
    print("Press 'a' will run the automatic program,press 'q' will quit.\nPress 's' will run the manually program, press 'w' will quit.")

    # 定义全局变量
    global gps_tow, gps_week, lat, lon, height,velocity,a_pressed, s_pressed

    # 创建一个socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接到指定的IP和端口
    s.connect(("10.0.1.1", 21000)) #修改：这里是连接到RTK的IP和端口，有线为networksetting中的Ethernet IP，无线为networksetting中的WIFI IP


    # 创建一个新的socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接到服务器
    client_socket.connect(("127.0.0.1", 23010))  # 修改：修改为要发送到的目标IP和端口
    
    read_second_string = False
    velocity = True
    first_lat, first_lon, first_height, mother_lat, mother_lon, mother_height, first_lat_s, first_lon_s, first_height_s, mother_lat_s, mother_lon_s, mother_height_s = None, None, None, None, None, None, None, None, None, None, None, None
    total_distance = 0
    total_distance_s = 0

    # 创建gps数据fix队列
    queue = deque(maxlen=8)

    # 环形存储区初始化
    data_storage = []
    print("distance software is running ...")

    while True:
        # 从socket读取数据
        data = s.recv(204800).decode(errors='ignore')

        # print(data)

        # 如果已经开始读取第二个字符串，就跳过第一个字符串的处理
        # 检查数据是否以"$FP,ODOMETRY"开始
        if data.startswith("$FP,ODOMETRY"):
            # 分割数据
            parts = data.split(',')
            #print("GNSS1 status:" ,parts[23],"GNSS2 status:",parts[24])

            # 检查速度是否大于等于0
            if parts[12]:
                if float(parts[12]) >= 0:
                    velocity = True
                else:
                    velocity = False
            else:
                print("VRTK2 running wrong,please check the status!")       

            # 将parts[23]和parts[24]的值添加到队列中
            queue.append((int(parts[23]), int(parts[24])))

            # 计算队列中等于8的元素的个数
            count = sum(1 for x, y in queue if x == 8 and y == 8)

            if len(queue) == 8:
                # 检查GNSS状态是否等于8
                if a_pressed and not read_second_string and count == 4:
                    read_second_string = True
                    print("Start calcuating distance ...")
                if a_pressed and read_second_string and count == 8:
                    read_second_string = False
                    first_lat, first_lon, first_height, mother_lat, mother_lon, mother_height = None, None, None,None,None,None
                    total_distance = 0
                    print("End calcuating distance ...")


        # 如果两个GNSS状态等于8，开始读取第二个字符串
        if data.startswith("$FP,LLH"):

            # 分割数据
            parts = data.split(',')
            # print(data)

            # 获取latitude, longitude, height, time
            if parts[3] and parts[4] and parts[5] and parts[6] and parts[7]:
                gps_week = int(parts[3])
                gps_tow = float(parts[4])
                lat = float(parts[5])
                lon = float(parts[6])
                height = float(parts[7])
                
            else:
                print("VRTK2 running wrong,please check the status! The LLH not output")
                gps_week = 0
                gps_tow = 0.0
                lat = 0.0
                lon = 0.0
                height = 0.0

            new_data = {
                'lat':lat,
                'lon':lon,
                'height':height,
                'gps_week':gps_week,
                'gps_tow':gps_tow,
                'velocity':velocity,
            }

            new_data['velocity'] = velocity

            # 将数据存储在环形存储区
            data_storage.append(new_data)

            # 如果环形存储区的长度大于8，删除第一个元素
            if len(data_storage) > 8:
                data_storage.pop(0)

            # 如果按下'a'键，开始自动计算距离
            if a_pressed:
                if read_second_string :
                    # 如果是首次读取，将经纬度和高度存储在常量中
                    if mother_lat is None and mother_lon is None and mother_height is None:
                        first_lat, first_lon, first_height = lat, lon, height

                        first_data = data_storage[0]
                        mother_lat, mother_lon, mother_height = first_data['lat'], first_data['lon'], first_data['height']
                        # mother_lat, mother_lon, mother_height = lat, lon, height

                        # 计算列表中的距离
                        previous_data = None
                        for data in data_storage:
                            # 如果previous_data不为None，就计算距离
                            if previous_data is not None:
                                distance = calculate_distance(previous_data['lat'], previous_data['lon'], previous_data['height'], data['lat'], data['lon'], data['height'])
                                # 如果速度为正，累加距离，否则减去距离
                                if data['velocity']:
                                    total_distance += distance
                                else:
                                    total_distance -= distance
                            # 更新previous_data
                            previous_data = data

                        
                    else:
                        # 计算新的位置与首次读取的位置之间的距离，并累加
                        distance = calculate_distance(first_lat, first_lon, first_height, lat, lon, height)

                        # 如果速度为正，累加距离，否则减去距离
                        if velocity:
                            total_distance += distance
                        if not velocity:
                            total_distance -= distance

                        # 打印累计距离
                        print("Total distance:", total_distance, "The distancce start from:",mother_lat, mother_lon, mother_height, "The distance end at:", lat, lon, height)
                        
                        # 发送数据，格式为： 时间，时间，距离，当前经纬高，记录起始点经纬高
                        data_string = "$FP,Auto,{},{},{},{},{},{},{},{},{}\n".format(gps_week, gps_tow, total_distance, lat, lon, height, mother_lat, mother_lon, mother_height)

                        

                        # 发送数据
                        client_socket.send(data_string.encode())

                        # 将新的数据设置为首次读取的数据
                        first_lat, first_lon, first_height = lat, lon, height
            
            # 如果按下's'键，开始手动计算距离
            if s_pressed:
                print("Manually calculating distance ...")
                if mother_lat_s is None and mother_lon_s is None and mother_height_s is None:
                    first_lat_s, first_lon_s, first_height_s = lat, lon, height
                    mother_lat_s, mother_lon_s, mother_height_s = lat, lon, height
                
                else:
                    # 计算新的位置与首次读取的位置之间的距离，并累加
                    distance_s = calculate_distance(first_lat_s, first_lon_s, first_height_s, lat, lon, height)

                    # 如果速度为正，累加距离，否则减去距离
                    if velocity:
                        total_distance_s += distance_s
                    if not velocity:
                        total_distance_s -= distance_s
                        # 发送数据，格式为： 时间，时间，距离，当前经纬高，记录起始点经纬高

                    data_string_s = "$FP,Manual,{},{},{},{},{},{},{},{},{}\n".format(gps_week, gps_tow, total_distance_s, lat, lon, height, mother_lat_s, mother_lon_s, mother_height_s)
                    

                    # 发送数据
                    client_socket.send(data_string_s.encode())

                    # 将新的数据设置为首次读取的数据
                    first_lat_s, first_lon_s, first_height_s = lat, lon, height
    # 关闭连接
    s.close()
    # 关闭客户端连接
    client_socket.close()






read_from_socket()