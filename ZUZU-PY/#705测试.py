import cv2
import time
from datetime import datetime, timedelta

# 获取当前北京时间，由于搜索结果可能会有些许延迟，我们可以直接使用内置的datetime库来获取准确时间
current_time = datetime.now()
# 计算当前时间+8小时
future_time = current_time + timedelta(hours=8)
# 格式化时间字符串
formatted_future_time = future_time.strftime("%Y-%m-%d %H:%M:%S")

# 打开文件，以追加模式写入空白2行、计算后的时间和空白1行
with open('IP_save.txt', 'a', encoding='utf-8') as file:
    file.write('\n' * 2)  # 写入空白2行
    file.write(formatted_future_time + '\n')  # 写入计算后的时间
    file.write('\n')  # 写入空白1行

print("文件操作已完成，已将当前时间+8小时的时间写入到'IP_save.txt'文件中。")
#############################################################################split##
#分割分割###################
#分割分割###################


import time

import concurrent.futures

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

import requests

import re

import os

import threading

from queue import Queue

from datetime import datetime

import replace

import fileinput

#上面载入需要在github运行的环境组件


# SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1
## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1
#提取IP前先合并自定义频道文件

file_contents = []   #这里含义是打开当前目录下以下文件清单--必须要保证有文件--否则报错

file_paths = ["山西联通.txt","安徽电信.txt", "河南联通.txt", "河南电信.txt", "福建电信.txt", "贵州电信.txt", "四川联通.txt", "四川电信.txt", "重庆联通.txt", "重庆电信.txt","山东电信.txt","广东电信.txt","广西电信.txt","江西电信.txt","河北电信.txt","浙江电信.txt","湖北电信.txt","湖南电信.txt","辽宁联通.txt","陕西电信.txt"]  #替换为实际的文件路径列表

for file_path in file_paths:

    with open(file_path, 'r', encoding="utf-8") as file:

        content = file.read()

        file_contents.append(content)


#写入2小时内更新的地址

with open("K合并2H.txt", "w", encoding="utf-8") as output:

    output.write('\n'.join(file_contents))
	
	

import cv2
import time

# 用于存储已经测试过的IP和结果，以及对应的帧数
tested_ips = {}

# 打开文件，并设置编码为utf-8
with open('K合并2H.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 检查行中是否包含1个逗号
        if line.count(',') == 1:
            # 将整行定义为一个channel
            channel = line.strip()
            
            # 截取IP和URL
            ip_start = line.find(',') + 1
            rtp_pos = line.find('rtp')
            if rtp_pos != -1:
                ip_part = line[ip_start:rtp_pos].strip()
            
            url_start = ip_start
            url_end = line.find('$')
            if url_end != -1:
                url = line[url_start:url_end].strip()
            else:
                # 如果没有找到$，则使用从,到行尾的部分
                url = line[url_start:].strip()
            
            # 检查IP是否已经被测试过
            if ip_part in tested_ips:
                # 如果IP已经存在，则跳过测试
                print(f"跳过已测试的IP: {ip_part}")
                continue

            # 使用cv2的VideoCapture来尝试打开视频流
            cap = cv2.VideoCapture(url)
            
            # 设置超时时间
            start_time = time.time()
            frame_count = 0
            
            # 尝试读取视频
            while frame_count < 9999 and (time.time() - start_time) < 10:  # 超时时间
                ret, frame = cap.read()
                if not ret:  # 检查是否成功读取到帧
                    break  # 如果没有读取到帧，则跳出循环
                frame_count += 1  # 成功读取一帧，计数器加1

            # 根据测试结果更新字典
            if frame_count > 220:  # 限定合格IP判定的帧数
                tested_ips[ip_part] = {'status': 'ok', 'frame_count': frame_count}
            else:
                # 如果没有读取到足够帧，则标记为已测试
                tested_ips[ip_part] = {'status': 'tested', 'frame_count': frame_count}

            # 释放VideoCapture对象
            cap.release()

# 测试结束后，将包含ok的IP的channel及其帧数写入新文件
with open('K合并2H-SPEED.txt', 'w', encoding='utf-8') as file:
    with open('K合并2H.txt', 'r', encoding='utf-8') as input_file:
        for line in input_file:
            # 检查行中是否包含1个逗号，以确保是channel
            if line.count(',') == 1:
                # 截取IP部分
                ip_start = line.find(',') + 1
                rtp_pos = line.find('rtp')
                if rtp_pos != -1:
                    channel_ip = line[ip_start:rtp_pos].strip()
                    
                    # 检查这个IP是否在测试成功的IP字典中
                    if channel_ip in tested_ips and tested_ips[channel_ip]['status'] == 'ok':
                        # 如果在，就写入这个channel和帧数到输出文件
                        # 注意：这里我们简单地在行末尾添加了帧数，你可以根据需要调整格式
                        file.write(f"{line}>速度={tested_ips[channel_ip]['frame_count']}\n")

	
	
	
	
	

	

# SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2
## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2
#提取IP前先合并自定义频道文件

file_contents = []   #这里含义是打开当前目录下以下文件清单--必须要保证有文件--否则报错

file_paths = ["天津联通.txt","江苏电信.txt"]  #低速线路专用

for file_path in file_paths:

    with open(file_path, 'r', encoding="utf-8") as file:

        content = file.read()

        file_contents.append(content)


#写入2小时内更新的地址

with open("K合并2H-低速线.txt", "w", encoding="utf-8") as output:

    output.write('\n'.join(file_contents))
	
	
import cv2
import time

# 用于存储已经测试过的IP和结果，以及对应的帧数
tested_ips = {}

# 打开文件，并设置编码为utf-8
with open('K合并2H-低速线.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 检查行中是否包含1个逗号
        if line.count(',') == 1:
            # 将整行定义为一个channel
            channel = line.strip()
            
            # 截取IP和URL
            ip_start = line.find(',') + 1
            rtp_pos = line.find('rtp')
            if rtp_pos != -1:
                ip_part = line[ip_start:rtp_pos].strip()
            
            url_start = ip_start
            url_end = line.find('$')
            if url_end != -1:
                url = line[url_start:url_end].strip()
            else:
                # 如果没有找到$，则使用从,到行尾的部分
                url = line[url_start:].strip()
            
            # 检查IP是否已经被测试过
            if ip_part in tested_ips:
                # 如果IP已经存在，则跳过测试
                print(f"跳过已测试的IP: {ip_part}")
                continue

            # 使用cv2的VideoCapture来尝试打开视频流
            cap = cv2.VideoCapture(url)
            
            # 设置超时时间
            start_time = time.time()
            frame_count = 0
            
            # 尝试读取视频
            while frame_count < 9999 and (time.time() - start_time) < 10:  # 超时时间
                ret, frame = cap.read()
                if not ret:  # 检查是否成功读取到帧
                    break  # 如果没有读取到帧，则跳出循环
                frame_count += 1  # 成功读取一帧，计数器加1

            # 根据测试结果更新字典
            if frame_count > 150:  # 限定合格IP判定的帧数
                tested_ips[ip_part] = {'status': 'ok', 'frame_count': frame_count}
            else:
                # 如果没有读取到足够帧，则标记为已测试
                tested_ips[ip_part] = {'status': 'tested', 'frame_count': frame_count}

            # 释放VideoCapture对象
            cap.release()

# 测试结束后，将包含ok的IP的channel及其帧数写入新文件
with open('K合并2H-低速线SPEED.txt', 'w', encoding='utf-8') as file:
    with open('K合并2H-低速线.txt', 'r', encoding='utf-8') as input_file:
        for line in input_file:
            # 检查行中是否包含1个逗号，以确保是channel
            if line.count(',') == 1:
                # 截取IP部分
                ip_start = line.find(',') + 1
                rtp_pos = line.find('rtp')
                if rtp_pos != -1:
                    channel_ip = line[ip_start:rtp_pos].strip()
                    
                    # 检查这个IP是否在测试成功的IP字典中
                    if channel_ip in tested_ips and tested_ips[channel_ip]['status'] == 'ok':
                        # 如果在，就写入这个channel和帧数到输出文件
                        # 注意：这里我们简单地在行末尾添加了帧数，你可以根据需要调整格式
                        file.write(f"{line}>速度={tested_ips[channel_ip]['frame_count']}\n")
	
	
