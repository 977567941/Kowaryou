import cv2 
import time

from datetime import datetime, timedelta

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

#载入组件

# merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1##
## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## merge-1## 
# 定义需要排除的IP列表
exclude_strings = ['//27.10', '//220.176.218', '//171.221.129', '//118.122.111', '//27.191.71', '//175.11.171', '//220.176.218', '//117.43.80', '//182.139.152', '//118.122.111', '//118.112.60', '//27.191.71', '//122.232.188', '//125.71.44', '//122.234.77', '//122.232.188', '//14.105.105.35', '//27.191.71.248', '//144.255.40.160', '//140.250.221', '//223.242.146', '//182.139.215', '//182.150.168', '//120.32.11', '//113.86.204.209', '//110.185.44', '///61.157.92.168', '//59.56.214', '//117.25.38', '//125.82.171', '//117.12.148', '//183.5.92', '//117.66.231', '//36.47.83', '//115.221.95', '//113.120.108', '//115.193.167', '//117.28.112', '//117.25.38', '//117.67.169', '//221.15.251', '//117.67.169', '//221.15.251', '//116.5.168', '//175.0.95', '//118.248.154', '//220.175.144', '//118.254.201', '//14.154.192', '//124.112.208', '//182.148.30', '//110.185.70', '//183.5.97.206', '//123.55.112', '//222.182.115', '//14.117.233', '//113.13.242', '//59.56.214.134', '//58.42.184.132', '//58.42.184.132', '//220.192.1.40', '//27.11.253.19', '//27.11.58.239', '//14.105.104', '//183.54.208.185', '//116.252.77.132', '//221.232.175', '//144.255.44.24', '//113.222.42.190', '//61.150.11', '//110.185.10', '//118.254', '//122.232.188', '//171.116.157', '//125.43.40', '//125.86.181', '//27.153.80', '//61.190.129.1', '//182.46.8', '//119.130.11', '//58.63.65', '//1.84.218', '//183.184', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+']

# 加载文件路径列表
file_paths = ["山西联通.txt", "安徽电信.txt", "河南联通.txt", "河南电信.txt", "福建电信.txt", "贵州电信.txt", "四川联通.txt", "四川电信.txt", "重庆联通.txt", "重庆电信.txt", "山东电信.txt", "广东电信.txt", "广西电信.txt", "江西电信.txt", "河北电信.txt", "浙江电信.txt", "湖北电信.txt", "湖南电信.txt", "辽宁联通.txt", "陕西电信.txt", "K合并OLD.txt"]

# 打开输出文件准备写入
with open("K合并2H+OLD.txt", "w", encoding="utf-8") as output:
    # 遍历文件路径列表
    for file_path in file_paths:
        # 打开当前文件并逐行读取
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                # 检查当前行是否不包含任何需要排除的字符串
                if not any(exclude_string in line for exclude_string in exclude_strings):
                    # 如果不包含，则写入到输出文件
                    output.write(line)


	
# SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1
## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1## SPEEDTEST-1

# 用于存储已经测试过的IP和结果，以及对应的帧数
tested_ips = {}

# 读取文件内容到列表中，避免重复打开文件
lines = []
with open('K合并2H+OLD.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 测试视频流
for line in lines:
    # 检查行中是否包含1个逗号
    if line.count(',') == 1:
        # 截取IP和URL
        ip_start = line.find(',') + 1
        rtp_pos = line.find('rtp')
        if rtp_pos != -1:
            ip_part = line[ip_start:rtp_pos].strip()
        else:
            # 如果没有找到'rtp'，则使用从逗号到行尾的部分作为IP（但请注意，这可能不是准确的IP）
            ip_part = line[ip_start:].strip()

        url_start = ip_start
        url_end = line.find('$')
        if url_end != -1:
            url = line[url_start:url_end].strip()
        else:
            # 如果没有找到'$'，则使用从逗号到行尾的部分作为URL（但请注意，这可能需要调整）
            url = line[url_start:].strip()

        # 检查IP是否已经被测试过
        if ip_part in tested_ips:
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
        if frame_count >220:  # 限定合格IP判定的帧数
            tested_ips[ip_part] = {'status': 'ok', 'frame_count': frame_count}
        else:
            tested_ips[ip_part] = {'status': 'tested', 'frame_count': frame_count}

        # 释放VideoCapture对象
        cap.release()

# 测试结束后，将包含ok的IP的channel及其帧数写入新文件
with open('K合并2H+OLD-SPEED.txt', 'w', encoding='utf-8') as file:
    for line in lines:
        # 检查行中是否包含1个逗号，以确保是channel
        if line.count(',') == 1:
            # 截取IP部分
            ip_start = line.find(',') + 1
            rtp_pos = line.find('rtp')
            if rtp_pos != -1:
                channel_ip = line[ip_start:rtp_pos].strip()

                # 检查这个IP是否在测试成功的IP字典中
                if channel_ip in tested_ips and tested_ips[channel_ip]['status'] == 'ok':
                    # 如果在，先写入原始行
                    file.write(f"{line.strip()}\n")
                    # 然后在下一行写入帧数信息
                    frame_count = tested_ips[channel_ip]['frame_count']
                    file.write(f">速度{frame_count}\n")
	

# merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2##
## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## merge-2## 
# 定义需要排除的IP列表
exclude_strings = ['//27.10', '//220.176.218', '//171.221.129', '//118.122.111', '//27.191.71', '//175.11.171', '//220.176.218', '//117.43.80', '//182.139.152', '//118.122.111', '//118.112.60', '//27.191.71', '//122.232.188', '//125.71.44', '//122.234.77', '//122.232.188', '//14.105.105.35', '//27.191.71.248', '//144.255.40.160', '//140.250.221', '//223.242.146', '//182.139.215', '//182.150.168', '//120.32.11', '//113.86.204.209', '//110.185.44', '///61.157.92.168', '//59.56.214', '//117.25.38', '//125.82.171', '//117.12.148', '//183.5.92', '//117.66.231', '//36.47.83', '//115.221.95', '//113.120.108', '//115.193.167', '//117.28.112', '//117.25.38', '//117.67.169', '//221.15.251', '//117.67.169', '//221.15.251', '//116.5.168', '//175.0.95', '//118.248.154', '//220.175.144', '//118.254.201', '//14.154.192', '//124.112.208', '//182.148.30', '//110.185.70', '//183.5.97.206', '//123.55.112', '//222.182.115', '//14.117.233', '//113.13.242', '//59.56.214.134', '//58.42.184.132', '//58.42.184.132', '//220.192.1.40', '//27.11.253.19', '//27.11.58.239', '//14.105.104', '//183.54.208.185', '//116.252.77.132', '//221.232.175', '//144.255.44.24', '//113.222.42.190', '//61.150.11', '//110.185.10', '//118.254', '//122.232.188', '//171.116.157', '//125.43.40', '//125.86.181', '//27.153.80', '//61.190.129.1', '//182.46.8', '//119.130.11', '//58.63.65', '//1.84.218', '//183.184', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+', '//+']

# 加载文件路径列表
file_paths = ["天津联通.txt","江苏电信.txt","K合并低码OLD.txt"]

# 打开输出文件准备写入
with open("K合并低码2H+低码OLD.txt", "w", encoding="utf-8") as output:
    # 遍历文件路径列表
    for file_path in file_paths:
        # 打开当前文件并逐行读取
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                # 检查当前行是否不包含任何需要排除的字符串
                if not any(exclude_string in line for exclude_string in exclude_strings):
                    # 如果不包含，则写入到输出文件
                    output.write(line)


# SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2
## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2## SPEEDTEST-2

# 用于存储已经测试过的IP和结果，以及对应的帧数
tested_ips = {}

# 读取文件内容到列表中，避免重复打开文件
lines = []
with open('K合并低码2H+低码OLD.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 测试视频流
for line in lines:
    # 检查行中是否包含1个逗号
    if line.count(',') == 1:
        # 截取IP和URL
        ip_start = line.find(',') + 1
        rtp_pos = line.find('rtp')
        if rtp_pos != -1:
            ip_part = line[ip_start:rtp_pos].strip()
        else:
            # 如果没有找到'rtp'，则使用从逗号到行尾的部分作为IP（但请注意，这可能不是准确的IP）
            ip_part = line[ip_start:].strip()

        url_start = ip_start
        url_end = line.find('$')
        if url_end != -1:
            url = line[url_start:url_end].strip()
        else:
            # 如果没有找到'$'，则使用从逗号到行尾的部分作为URL（但请注意，这可能需要调整）
            url = line[url_start:].strip()

        # 检查IP是否已经被测试过
        if ip_part in tested_ips:
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
        if frame_count >220:  # 限定合格IP判定的帧数
            tested_ips[ip_part] = {'status': 'ok', 'frame_count': frame_count}
        else:
            tested_ips[ip_part] = {'status': 'tested', 'frame_count': frame_count}

        # 释放VideoCapture对象
        cap.release()

# 测试结束后，将包含ok的IP的channel及其帧数写入新文件
with open('K合并低码2H+低码OLD-SPEED.txt', 'w', encoding='utf-8') as file:
    for line in lines:
        # 检查行中是否包含1个逗号，以确保是channel
        if line.count(',') == 1:
            # 截取IP部分
            ip_start = line.find(',') + 1
            rtp_pos = line.find('rtp')
            if rtp_pos != -1:
                channel_ip = line[ip_start:rtp_pos].strip()

                # 检查这个IP是否在测试成功的IP字典中
                if channel_ip in tested_ips and tested_ips[channel_ip]['status'] == 'ok':
                    # 如果在，先写入原始行
                    file.write(f"{line.strip()}\n")
                    # 然后在下一行写入帧数信息
                    frame_count = tested_ips[channel_ip]['frame_count']
                    file.write(f">速度{frame_count}\n")






# SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3
## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3## SPEEDTEST-3

# 用于存储已经测试过的IP和结果，以及对应的帧数
tested_ips = {}

# 读取文件内容到列表中，避免重复打开文件
lines = []
with open('JX-LOW.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 测试视频流
for line in lines:
    # 检查行中是否包含1个逗号
    if line.count(',') == 1:
        # 截取IP和URL
        ip_start = line.find(',') + 1
        rtp_pos = line.find('rtp')
        if rtp_pos != -1:
            ip_part = line[ip_start:rtp_pos].strip()
        else:
            # 如果没有找到'rtp'，则使用从逗号到行尾的部分作为IP（但请注意，这可能不是准确的IP）
            ip_part = line[ip_start:].strip()

        url_start = ip_start
        url_end = line.find('$')
        if url_end != -1:
            url = line[url_start:url_end].strip()
        else:
            # 如果没有找到'$'，则使用从逗号到行尾的部分作为URL（但请注意，这可能需要调整）
            url = line[url_start:].strip()

        # 检查IP是否已经被测试过
        if ip_part in tested_ips:
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
        if frame_count >210:  # 限定合格IP判定的帧数
            tested_ips[ip_part] = {'status': 'ok', 'frame_count': frame_count}
        else:
            tested_ips[ip_part] = {'status': 'tested', 'frame_count': frame_count}

        # 释放VideoCapture对象
        cap.release()

# 测试结束后，将包含ok的IP的channel及其帧数写入新文件
with open('JX-LOW-SPEED.txt', 'w', encoding='utf-8') as file:
    for line in lines:
        # 检查行中是否包含1个逗号，以确保是channel
        if line.count(',') == 1:
            # 截取IP部分
            ip_start = line.find(',') + 1
            rtp_pos = line.find('rtp')
            if rtp_pos != -1:
                channel_ip = line[ip_start:rtp_pos].strip()

                # 检查这个IP是否在测试成功的IP字典中
                if channel_ip in tested_ips and tested_ips[channel_ip]['status'] == 'ok':
                    # 如果在，先写入原始行
                    file.write(f"{line.strip()}\n")
                    # 然后在下一行写入帧数信息
                    frame_count = tested_ips[channel_ip]['frame_count']
                    file.write(f">速度{frame_count}\n")





# SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4
## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4## SPEEDTEST-4

# 用于存储已经测试过的IP和结果，以及对应的帧数
tested_ips = {}

# 读取文件内容到列表中，避免重复打开文件
lines = []
with open('JX-HIGH.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 测试视频流
for line in lines:
    # 检查行中是否包含1个逗号
    if line.count(',') == 1:
        # 截取IP和URL
        ip_start = line.find(',') + 1
        rtp_pos = line.find('rtp')
        if rtp_pos != -1:
            ip_part = line[ip_start:rtp_pos].strip()
        else:
            # 如果没有找到'rtp'，则使用从逗号到行尾的部分作为IP（但请注意，这可能不是准确的IP）
            ip_part = line[ip_start:].strip()

        url_start = ip_start
        url_end = line.find('$')
        if url_end != -1:
            url = line[url_start:url_end].strip()
        else:
            # 如果没有找到'$'，则使用从逗号到行尾的部分作为URL（但请注意，这可能需要调整）
            url = line[url_start:].strip()

        # 检查IP是否已经被测试过
        if ip_part in tested_ips:
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
        if frame_count >150:  # 限定合格IP判定的帧数
            tested_ips[ip_part] = {'status': 'ok', 'frame_count': frame_count}
        else:
            tested_ips[ip_part] = {'status': 'tested', 'frame_count': frame_count}

        # 释放VideoCapture对象
        cap.release()

# 测试结束后，将包含ok的IP的channel及其帧数写入新文件
with open('JX-HIGH-SPEED.txt', 'w', encoding='utf-8') as file:
    for line in lines:
        # 检查行中是否包含1个逗号，以确保是channel
        if line.count(',') == 1:
            # 截取IP部分
            ip_start = line.find(',') + 1
            rtp_pos = line.find('rtp')
            if rtp_pos != -1:
                channel_ip = line[ip_start:rtp_pos].strip()

                # 检查这个IP是否在测试成功的IP字典中
                if channel_ip in tested_ips and tested_ips[channel_ip]['status'] == 'ok':
                    # 如果在，先写入原始行
                    file.write(f"{line.strip()}\n")
                    # 然后在下一行写入帧数信息
                    frame_count = tested_ips[channel_ip]['frame_count']
                    file.write(f">速度{frame_count}\n")



#分割分割###################
#分割分割###################
#分割分割###################
#分割分割###################
#分割分割###################
#分割分割###################
#分割分割###################
#分割分割###################




# 写回+去重复操作1
with open('K合并2H+OLD-SPEED.txt', 'r', encoding='utf-8') as file_in:
    # 打开或创建文件以写入内容
    with open('K合并2H+OLD-SPEEDjump.txt', 'w', encoding='utf-8') as file_out:
        # 逐行读取
        for line in file_in:
            # 将读取到的内容写入
            file_out.write(line)

# 去重复--定义一个集合来存储已经遇到的URL，以便检查重复
# 定义一个集合用于存储已经遇到的行
seen_lines = set()

# 使用 'with' 语句确保文件在操作完成后正确关闭
with open('K合并2H+OLD-SPEEDjump.txt', 'r', encoding='utf-8') as file_in, \
     open('K合并OLD.txt', 'w', encoding='utf-8') as file_out:
    # 逐行读取文件
    for line in file_in:
        # 去除行尾的换行符，并检查该行是否已经在集合中
        stripped_line = line.strip()
        if stripped_line not in seen_lines:
            # 如果不在集合中，将其写入添加到集合中
            file_out.write(line)
            seen_lines.add(stripped_line)
			
			

# 写回+去重复操作2
with open('K合并低码2H+低码OLD-SPEED.txt', 'r', encoding='utf-8') as file_in:
    # 打开或创建文件以写入内容
    with open('K合并低码2H+低码OLD-SPEEDjump.txt', 'w', encoding='utf-8') as file_out:
        # 逐行读取
        for line in file_in:
            # 将读取到的内容写入
            file_out.write(line)

# 去重复--定义一个集合来存储已经遇到的URL，以便检查重复
# 定义一个集合用于存储已经遇到的行
seen_lines = set()

# 使用 'with' 语句确保文件在操作完成后正确关闭
with open('K合并低码2H+低码OLD-SPEEDjump.txt', 'r', encoding='utf-8') as file_in, \
     open('K合并低码OLD.txt', 'w', encoding='utf-8') as file_out:
    # 逐行读取文件
    for line in file_in:
        # 去除行尾的换行符，并检查该行是否已经在集合中
        stripped_line = line.strip()
        if stripped_line not in seen_lines:
            # 如果不在集合中，将其写入添加到集合中
            file_out.write(line)
            seen_lines.add(stripped_line)





#IP_SAVE运作流程

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

#1############################################################################split##


#根据前面合并IP，一次顺序添加到IP_SAVE.txt  a模式
# 需要提取的关键字列表
keywords = ['S川A爱科幻','天JD都市高清','安HH生活时尚','山DB农科','山XD都市剧场','广DA经济科教','广XH南宁都市','江S南京生活','江XB都市剧场','河BA农民高清','河N民生频道','河NC电视剧频道','浙JC教育高清','湖N常德新闻','福JA少儿','辽LD沈阳新闻','重QD影视频道','陕XA新闻资讯']  
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('K合并2H+OLD.txt', 'r', encoding='utf-8') as file, open('IP_save.txt', 'a', encoding='utf-8') as IP_save:

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         IP_save.write(line)  # 将该行写入文件
		 
		 
#根据前面合并低码IP，二次顺序添加到IP_SAVE.txt  a模式
# 需要提取的关键字列表		 
keywords = ['S川A爱科幻','天JD都市高清','安HH生活时尚','山DB农科','山XD都市剧场','广DA经济科教','广XH南宁都市','江S南京生活','江XB都市剧场','河BA农民高清','河N民生频道','河NC电视剧频道','浙JC教育高清','湖N常德新闻','福JA少儿','辽LD沈阳新闻','重QD影视频道','陕XA新闻资讯']  
pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制	 
with open('K合并低码2H+低码OLD.txt', 'r', encoding='utf-8') as file, open('IP_save.txt', 'a', encoding='utf-8') as IP_save:

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         IP_save.write(line)  # 将该行写入文件		 

#########################split##



# 写回+去重复操作
with open('IP_save.txt', 'r', encoding='utf-8') as file_in:
    # 打开或创建IP_savejump.txt文件以写入内容
    with open('IP_savejump.txt', 'w', encoding='utf-8') as file_out:
        # 逐行读取IP_save.txt的内容
        for line in file_in:
            # 将读取到的内容写入IP_savejump.txt
            file_out.write(line)

# 去重复--定义一个集合来存储已经遇到的URL，以便检查重复
# 定义一个集合用于存储已经遇到的行
seen_lines = set()

# 使用 'with' 语句确保文件在操作完成后正确关闭
with open('IP_savejump.txt', 'r', encoding='utf-8') as file_in, \
     open('IP_save.txt', 'w', encoding='utf-8') as file_out:
    # 逐行读取 IP_savejump.txt 文件
    for line in file_in:
        # 去除行尾的换行符，并检查该行是否已经在集合中
        stripped_line = line.strip()
        if stripped_line not in seen_lines:
            # 如果不在集合中，将其写入到 IP_save.txt 并添加到集合中
            file_out.write(line)
            seen_lines.add(stripped_line)
			
			
			
			
#分割分割###################
#分割分割###################
#分割分割###################
#分割分割###################
#分割分割###################
#分割分割###################
#分割分割###################
#分割分割###################





#合并自定义频道文件########
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

#重新载入一遍运行环境############################


file_contents = []   #打开当前目录下以下文件清单

#此处-------K合并OLD.txt和K合并低码OLD.txt-------实际已经测速过写回去了--现在是调用
file_paths = ['K合并OLD.txt','K合并低码OLD.txt','JX-LOW-SPEED.txt','JX-HIGH-SPEED.txt',"JIEXI-OK.txt"]  #把测速结果合并到一起 



for file_path in file_paths:

    with open(file_path, 'r', encoding="utf-8") as file:

        content = file.read()

        file_contents.append(content)


#写入合并后的文件

with open("合并.txt", "w", encoding="utf-8") as output:

    output.write('\n'.join(file_contents))


#替换多余的关键字词###################################################################################################

for line in fileinput.input("合并.txt", inplace=True):  #打开文件，并对其进行原地替换

    line = line.replace("CCTV10", "CCTW10")

    line = line.replace("CCTV11", "CCTW11")

    line = line.replace("CCTV12", "CCTW12")

    line = line.replace("CCTV13", "CCTW13")

    line = line.replace("CCTV14", "CCTW14")

    line = line.replace("CCTV15", "CCTW15")

    line = line.replace("CCTV16", "CCTW16")

    line = line.replace("CCTV17", "CCTW17")

    #需要排在前面的频道

    line = line.replace("CCTV1综合", "CCTV1")

    line = line.replace("CCTV2财经", "CCTV2")

    line = line.replace("CCTV3综艺", "CCTV3")

    line = line.replace("CCTV4国际", "CCTV4")

    line = line.replace("CCTV4中文国际", "CCTV4")

    line = line.replace("CCTV4欧洲", "CCTV4")

    line = line.replace("CCTV5体育", "CCTV5")

    line = line.replace("CCTV5+体育", "CCTV5+")

    line = line.replace("CCTV6电影", "CCTV6")

    line = line.replace("CCTV7军事", "CCTV7")

    line = line.replace("CCTV7军农", "CCTV7")

    line = line.replace("CCTV7农业", "CCTV7")

    line = line.replace("CCTV7国防军事", "CCTV7")

    line = line.replace("CCTV8电视剧", "CCTV8")

    line = line.replace("CCTV8纪录", "CCTV9")

    line = line.replace("CCTV9记录", "CCTV9")

    line = line.replace("CCTV9纪录", "CCTV9")

    line = line.replace("CCTV10科教", "CCTV10")

    line = line.replace("CCTV11戏曲", "CCTV11")

    line = line.replace("CCTV12社会与法", "CCTV12")

    line = line.replace("CCTV13新闻", "CCTV13")

    line = line.replace("CCTV新闻", "CCTV13")

    line = line.replace("CCTV14少儿", "CCTV14")

    line = line.replace("央视14少儿", "CCTV14")

    line = line.replace("CCTV少儿超", "CCTV14")

    line = line.replace("CCTV15音乐", "CCTV15")

    line = line.replace("CCTV音乐", "CCTV15")

    line = line.replace("CCTV16奥林匹克", "CCTV16")

    line = line.replace("CCTV17农业农村", "CCTV17")

    line = line.replace("CCTV17军农", "CCTV17")

    line = line.replace("CCTV17农业", "CCTV17")

    line = line.replace("CCTV5+体育赛视", "CCTV5+")

    line = line.replace("CCTV5+赛视", "CCTV5+")

    line = line.replace("CCTV5+体育赛事", "CCTV5+")

    line = line.replace("CCTV5+赛事", "CCTV5+")

    line = line.replace("CCTV5+体育", "CCTV5+")

    line = line.replace("CCTV5赛事", "CCTV5+")



    print(line, end="")  #设置end=""，避免输出多余的换行符



#二次替换某些关键词为便于排序的自定义词####################################################################################################

for line in fileinput.input("合并.txt", inplace=True):  #打开文件，并对其进行原地替换

    
    line = line.replace("CCTV10", "CCTW10")

    line = line.replace("CCTV11", "CCTW11")

    line = line.replace("CCTV12", "CCTW12")

    line = line.replace("CCTV13", "CCTW13")

    line = line.replace("CCTV14", "CCTW14")

    line = line.replace("CCTV15", "CCTW15")

    line = line.replace("CCTV16", "CCTW16")

    line = line.replace("CCTV17", "CCTW17")


    print(line, end="")  #设置end=""，避免输出多余的换行符



#对替换完成的文本进行排序#####################################################################################################################



with open('合并.txt', 'r', encoding='utf-8') as f:

    lines = f.readlines()


lines.sort()


with open('排序.txt', 'w', encoding='UTF-8') as f:

    for line in lines:

        f.write(line)


#再次替换自定义词为常规词##########################################################################################################################

for line in fileinput.input("排序.txt", inplace=True):  #打开文件，并对其进行原地替换

    line = line.replace("CCTW10", "CCTV10")

    line = line.replace("CCTW11", "CCTV11")

    line = line.replace("CCTW12", "CCTV12")

    line = line.replace("CCTW13", "CCTV13")

    line = line.replace("CCTW14", "CCTV14")

    line = line.replace("CCTW15", "CCTV15")

    line = line.replace("CCTW16", "CCTV16")

    line = line.replace("CCTW17", "CCTV17")


    print(line, end="")  #设置end=""，避免输出多余的换行符

 ##################################################################################################################################SPLIT#


#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['CCTV','CETV', 'CF', 'IPT淘', 'CHC', 'IWA', '凤凰卫视', '卫视', '金鹰卡通', '纪实科教', '卡酷少儿', '嘉佳卡通', '哈哈炫动', '乐游频道', '动漫秀场', '新动漫','纪实人文', '金色学堂',  '纪实科教', '金鹰纪实', '求索记录']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T1.txt', 'w', encoding='utf-8') as T1:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T1.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T1.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT1.txt', 'w', encoding='utf-8') as TT1:    #####定义临时文件名

    TT1.write('\n📺中央数字超高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T1.txt', 'r', encoding="utf-8") as input_file, open('TT1.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################

 ##################################################################################################################################SPLIT#

#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['电Y']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T2.txt', 'w', encoding='utf-8') as T2:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T2.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T2.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT2.txt', 'w', encoding='utf-8') as TT2:    #####定义临时文件名

    TT2.write('\n🎬电影轮播标清频道,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T2.txt', 'r', encoding="utf-8") as input_file, open('TT2.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################



    ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['老DY']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T4.txt', 'w', encoding='utf-8') as T4:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T4.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T4.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT4.txt', 'w', encoding='utf-8') as TT4:    #####定义临时文件名

    TT4.write('\n🎬老电影黑白频道,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T4.txt', 'r', encoding="utf-8") as input_file, open('TT4.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
    ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['重Q']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T5.txt', 'w', encoding='utf-8') as T5:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T5.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T5.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT5.txt', 'w', encoding='utf-8') as TT5:    #####定义临时文件名

    TT5.write('\n👑重庆数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T5.txt', 'r', encoding="utf-8") as input_file, open('TT5.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
    ##################################################################################################################################SPLIT#
   
   #开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['北J']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T6.txt', 'w', encoding='utf-8') as T6:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T6.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T6.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT6.txt', 'w', encoding='utf-8') as TT6:    #####定义临时文件名

    TT6.write('\n👑北京数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T6.txt', 'r', encoding="utf-8") as input_file, open('TT6.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
    ##################################################################################################################################SPLIT#
   
      #开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['河B']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T7.txt', 'w', encoding='utf-8') as T7:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T7.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T7.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT7.txt', 'w', encoding='utf-8') as TT7:    #####定义临时文件名

    TT7.write('\n👑河北数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, int(sort_key))  # 数字从小到大排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T7.txt', 'r', encoding="utf-8") as input_file, open('TT7.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
##################################################################################################################################SPLIT#


#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['河N']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T8.txt', 'w', encoding='utf-8') as T8:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T8.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T8.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT8.txt', 'w', encoding='utf-8') as TT8:    #####定义临时文件名

    TT8.write('\n👑河南数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

# A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T8.txt', 'r', encoding="utf-8") as input_file, open('TT8.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   
 ##################################################################################################################################SPLIT#

#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['天J']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T9.txt', 'w', encoding='utf-8') as T9:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T9.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T9.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT9.txt', 'w', encoding='utf-8') as TT9:    #####定义临时文件名

    TT9.write('\n👑天津数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, int(sort_key))  # 数字从小到大排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T9.txt', 'r', encoding="utf-8") as input_file, open('TT9.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   
   
 ##################################################################################################################################SPLIT#

#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['广D']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T10.txt', 'w', encoding='utf-8') as T10:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T10.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T10.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT10.txt', 'w', encoding='utf-8') as TT10:    #####定义临时文件名

    TT10.write('\n👑广东数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T10.txt', 'r', encoding="utf-8") as input_file, open('TT10.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   
 ##################################################################################################################################SPLIT#
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['广X']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T11.txt', 'w', encoding='utf-8') as T11:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T11.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T11.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT11.txt', 'w', encoding='utf-8') as TT11:    #####定义临时文件名

    TT11.write('\n👑广西数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, int(sort_key))  # 数字从小到大排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T11.txt', 'r', encoding="utf-8") as input_file, open('TT11.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   
 ##################################################################################################################################SPLIT# 

#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['湖B']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T12.txt', 'w', encoding='utf-8') as T12:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T12.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T12.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT12.txt', 'w', encoding='utf-8') as TT12:    #####定义临时文件名

    TT12.write('\n👑湖北数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T12.txt', 'r', encoding="utf-8") as input_file, open('TT12.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################

 ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['山DA','山DB','山DC','山DD','山DE','山DF','山DG','山DK','山DZ']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T13.txt', 'w', encoding='utf-8') as T13:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T13.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T13.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT13.txt', 'w', encoding='utf-8') as TT13:    #####定义临时文件名

    TT13.write('\n👑山东数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T13.txt', 'r', encoding="utf-8") as input_file, open('TT13.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['安H']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T14.txt', 'w', encoding='utf-8') as T14:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T14.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T14.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT14.txt', 'w', encoding='utf-8') as TT14:    #####定义临时文件名

    TT14.write('\n👑安徽数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, int(sort_key))  # 数字从小到大排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T14.txt', 'r', encoding="utf-8") as input_file, open('TT14.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['江S']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T15.txt', 'w', encoding='utf-8') as T15:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T15.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T15.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT15.txt', 'w', encoding='utf-8') as TT15:    #####定义临时文件名

    TT15.write('\n👑江苏数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T15.txt', 'r', encoding="utf-8") as input_file, open('TT15.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['江XA','江XB','江XC','江XD','江XE']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T16.txt', 'w', encoding='utf-8') as T16:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T16.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T16.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT16.txt', 'w', encoding='utf-8') as TT16:    #####定义临时文件名

    TT16.write('\n👑江西数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T16.txt', 'r', encoding="utf-8") as input_file, open('TT16.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['山X']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T17.txt', 'w', encoding='utf-8') as T17:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T17.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T17.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT17.txt', 'w', encoding='utf-8') as TT17:    #####定义临时文件名

    TT17.write('\n👑山西数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T17.txt', 'r', encoding="utf-8") as input_file, open('TT17.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
 
 ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['浙J']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T18.txt', 'w', encoding='utf-8') as T18:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T18.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T18.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT18.txt', 'w', encoding='utf-8') as TT18:    #####定义临时文件名

    TT18.write('\n👑浙江数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T18.txt', 'r', encoding="utf-8") as input_file, open('TT18.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['湖N']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T19.txt', 'w', encoding='utf-8') as T19:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T19.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T19.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT19.txt', 'w', encoding='utf-8') as TT19:    #####定义临时文件名

    TT19.write('\n👑湖南数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T19.txt', 'r', encoding="utf-8") as input_file, open('TT19.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['辽L']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T20.txt', 'w', encoding='utf-8') as T20:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T20.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T20.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT20.txt', 'w', encoding='utf-8') as TT20:    #####定义临时文件名

    TT20.write('\n👑辽宁数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, int(sort_key))  # 数字从小到大排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T20.txt', 'r', encoding="utf-8") as input_file, open('TT20.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['吉L']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T21.txt', 'w', encoding='utf-8') as T21:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T21.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T21.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT21.txt', 'w', encoding='utf-8') as TT21:    #####定义临时文件名

    TT21.write('\n👑吉林地方频道,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T21.txt', 'r', encoding="utf-8") as input_file, open('TT21.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['贵Z','习水']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T22.txt', 'w', encoding='utf-8') as T22:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T22.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T22.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT22.txt', 'w', encoding='utf-8') as TT22:    #####定义临时文件名

    TT22.write('\n👑贵州地方频道,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

#A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T22.txt', 'r', encoding="utf-8") as input_file, open('TT22.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['陕X']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T23.txt', 'w', encoding='utf-8') as T23:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T23.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T23.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT23.txt', 'w', encoding='utf-8') as TT23:    #####定义临时文件名

    TT23.write('\n👑陕西数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

# A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, int(sort_key))  # 数字从小到大排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T23.txt', 'r', encoding="utf-8") as input_file, open('TT23.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
      ##################################################################################################################################SPLIT#
   
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['新J']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T24.txt', 'w', encoding='utf-8') as T24:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T24.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T24.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT24.txt', 'w', encoding='utf-8') as TT24:    #####定义临时文件名

    TT24.write('\n👑新疆数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

# A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T24.txt', 'r', encoding="utf-8") as input_file, open('TT24.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   
   
         ##################################################################################################################################SPLIT#
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['S川']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T25.txt', 'w', encoding='utf-8') as T25:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T25.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T25.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT25.txt', 'w', encoding='utf-8') as TT25:    #####定义临时文件名

    TT25.write('\n👑四川数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

# A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T25.txt', 'r', encoding="utf-8") as input_file, open('TT25.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

   #结束########################################################
   ##################################################################################################################################SPLIT#
           
#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['福JA','福JB','福JC']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T26.txt', 'w', encoding='utf-8') as T26:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T26.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T26.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT26.txt', 'w', encoding='utf-8') as TT26:    #####定义临时文件名

    TT26.write('\n👑福建数字高清,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

# A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T26.txt', 'r', encoding="utf-8") as input_file, open('TT26.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)

#结束########################################################
##################################################################################################################################SPLIT#

#开始#########################
#从整理好的文本中按类别进行特定关键词提取#############################################################################################

keywords = ['GAT']  # 需要提取的关键字列表

pattern = '|'.join(keywords)  # 创建正则表达式模式，匹配任意一个关键字

#pattern = r"^(.*?),(?!#genre#)(.*?)$" #以分类直接复制

with open('排序.txt', 'r', encoding='utf-8') as file, open('T30.txt', 'w', encoding='utf-8') as T30:    #####定义临时文件名

    for line in file:

        if re.search(pattern, line) and line.count(',') == 1:  # 如果行中有任意关键字而且行内只有一个逗号

         T30.write(line)  # 将该行写入输出文件 #####定义临时文件

for line in fileinput.input("T30.txt", inplace=True):  #打开文件，并对其进行关键词原地替换    

    print(line, end="")  #设置end=""，避免输出多余的换行符          

#新建待合并临时TTxxx.TXT文件并在抬头写入频道编码genre###################
with open('TT30.txt', 'w', encoding='utf-8') as TT30:    #####定义临时文件名

    TT30.write('\n👑中国香港澳门,#genre#\n')        
 
    print(line, end="")  #设置end=""，避免输出多余的换行符 
#写入完成-进入下一步排序######################

#对相同频道IP排序--域名在前###################
import re

# A版本--自定义排序键函数 固定域名--在前
def custom_sort_key(item):
    channel, url = item.split(',')

    channel_letters = ''.join(filter(str.isalpha, channel))
    channel_numbers = ''.join(filter(str.isdigit, channel))

    if channel_numbers.isdigit():
        channel_sort_key = (channel_letters, int(channel_numbers))
    else:
        channel_sort_key = (channel_letters, 0)

    sort_key = re.search(r"http://(.*?)\.", url)
    if sort_key:
        sort_key = sort_key.group(1)
    else:
        sort_key = url

    # 检查sort_key是否为数字
    if sort_key[0].isalpha():
        sort_key = (0, sort_key)  # 字母开头的sort_key排在最前面
    elif sort_key.isdigit():
        sort_key = (1, -int(sort_key))  # 数字从大到小排序
    else:
        sort_key = (2, sort_key)

    return (channel_sort_key, sort_key)

with open('T30.txt', 'r', encoding="utf-8") as input_file, open('TT30.txt', 'a', encoding="utf-8") as output_file:
    # 读取所有行并存储在列表中
    lines = input_file.readlines()

    # 过滤掉空白行
    lines = [line.strip() for line in lines if line.strip()]
    
    sorted_data = sorted(lines, key=custom_sort_key)

    # 将排序后的数据写入输出文件
    for channels in sorted_data: 
        output_file.write(f"{channels}\n")
    sorted_data = sorted(lines, key=custom_sort_key)
#结束########################################################
   
   
##################################################################################################################################SPLIT#
#开始合并多个文件到一个文件###########

file_contents = []

file_paths = ["TT1.txt", "TT2.txt", "TT4.txt", "TT5.txt", "TT6.txt", "TT7.txt", "TT8.txt", "TT9.txt", "TT10.txt", "TT11.txt", "TT12.txt", "TT13.txt", "TT14.txt", "TT15.txt", "TT16.txt", "TT17.txt", "TT18.txt", "TT19.txt", "TT20.txt", "TT21.txt", "TT22.txt", "TT23.txt", "TT24.txt", "TT25.txt", "TT26.txt", "TT30.txt"] 

for file_path in file_paths:

    with open(file_path, 'r', encoding="utf-8") as file:

        content = file.read()

        file_contents.append(content)



# 写入合并后的文件

with open("AMER-start.txt", "w", encoding="utf-8") as output:

    output.write('\n'.join(file_contents))

#结束合并
##################################################################################################################################SPLIT#
  
  

#开始对输出文件Americam.txt修改违规字操作如下
with open('AMER-start.txt', 'r', encoding='utf-8') as file:
    content = file.read()

#键入需要修改关键字
content = content.replace("福JA", "福建").replace("福JB", "福建").replace("福JC", "福建").replace("WA", "").replace("WB", "").replace("WC", "").replace("WD", "").replace("WE", "").replace("WF", "").replace("WG", "").replace("WH", "").replace("WI", "").replace("WJ", "").replace("WK", "").replace("WL", "").replace("WM", "").replace("WN", "").replace("WO", "").replace("WP", "").replace("WP", "").replace("WQ", "").replace("WR", "").replace("WS", "").replace("WT", "").replace("WU", "").replace("WV", "").replace("WW", "").replace("WX", "").replace("WY", "").replace("WZ", "").replace("CF", "").replace("IV", "").replace("X纪实", "X纪实").replace("Y卡酷", "卡酷").replace("Y动漫", "动漫").replace("Y金色学堂", "金色学堂").replace("电Y", "电影").replace("老DY", "老电影").replace("X乐", "乐").replace("X求", "求").replace("X纪", "纪").replace("X记", "记").replace("X金", "金").replace("Y动", "动").replace("Y卡", "卡").replace("Y咔", "咔").replace("Y嘉", "嘉").replace("Y新", "新").replace("剧J", "连续剧").replace("重Q", "重庆").replace("北J", "北京").replace("河B", "河北").replace("河N", "河南").replace("天J", "天津").replace("广D", "广东").replace("湖B", "湖北").replace("湖N", "湖南").replace("山D", "山东").replace("安H", "安徽").replace("江S", "江苏").replace("山X", "山西").replace("浙J", "浙江").replace("辽L", "辽宁").replace("吉L", "吉林").replace("贵Z", "贵州").replace("陕X", "陕西").replace("S川", "四川").replace("褔J", "福建").replace("GAT-", "").replace("裾J", "裾集").replace("江X", "江西").replace("新J", "新疆").replace("褔JA", "福建").replace("褔JB", "福建").replace("褔JC", "福建").replace("褔JD", "福建").replace("广X", "广西").replace("A", "").replace("B", "").replace("F", "").replace("G", "").replace("I", "").replace("J", "").replace("K", "").replace("L", "").replace("M", "").replace("N", "").replace("O", "").replace("P", "").replace("Q", "").replace("R", "").replace("S", "").replace("U", "").replace("W", "").replace("X", "").replace("Y", "").replace("Z", "").replace("C新闻", "新闻").replace("电映C", "电映").replace("电映E", "电映").replace("电映H", "电映").replace("D影视", "影视").replace("E都市", "都市").replace("H新农", "新农").replace("河北C", "河北").replace("河北D", "河北").replace("河南C", "河南").replace("河南D", "河南").replace("天津C", "天津").replace("天津D", "天津").replace("天津E", "天津").replace("广东C", "广东").replace("广东H", "广东").replace("广西C", "广西").replace("广西D", "广西").replace("广西E", "广西").replace("广西H", "广西").replace("湖北C", "湖北").replace("湖北D", "湖北").replace("山东C", "山东").replace("山东D", "山东").replace("山东E", "山东").replace("山东H", "山东").replace("安徽C", "安徽").replace("安徽D", "安徽").replace("安徽E", "安徽").replace("安徽H", "安徽").replace("江西C", "江西").replace("江西D", "江西").replace("江西E", "江西").replace("江西H", "江西").replace("陕西C", "陕西").replace("陕西D", "陕西").replace("陕西E", "陕西").replace("陕西H", "陕西").replace("浙江C", "浙江").replace("浙江D", "浙江").replace("浙江E", "浙江").replace("浙江H", "浙江").replace("四川C", "四川").replace("四川D", "四川").replace("四川E", "四川").replace("四川H", "四川").replace("辽宁C", "辽宁").replace("辽宁D", "辽宁").replace("辽宁E", "辽宁").replace("辽宁H", "辽宁").replace("吉林C", "吉林").replace("山西C", "山西").replace("山西D", "山西").replace("山西E", "山西").replace("山西H", "山西").replace("少_儿", "少儿").replace("少*儿", "少儿")

with open('AMER-delete.txt', 'w', encoding='utf-8') as file:
    file.write(content)
	
#结束对关键字替换
	
  ##################################################################################################################################SPLIT#
  

#开始去重复-打开文档并读取所有行 
with open('AMER-delete.txt', 'r', encoding="utf-8") as file:
 lines = file.readlines()
 
#使用列表来存储唯一的行的顺序 
 unique_lines = [] 
 seen_lines = set() 

#遍历每一行，如果是新的就加入unique_lines 
for line in lines:
 if line not in seen_lines:
  unique_lines.append(line)
  seen_lines.add(line)

#将唯一的行写入新的文档 
with open('yesterdayoncemo.txt', 'w', encoding="utf-8") as file:
 file.writelines(unique_lines)

#结束去重复

##################################################################################################################################SPLIT#

#删除所有临时文件--删除清单在下面列出

os.remove("IP_savejump.txt")

os.remove("AMER-delete.txt")

os.remove("AMER-start.txt")

os.remove("合并.txt")

os.remove("排序.txt")

os.remove("T1.txt")

os.remove("T2.txt")

os.remove("T4.txt")

os.remove("T5.txt")

os.remove("T6.txt")

os.remove("T7.txt")

os.remove("T8.txt")

os.remove("T9.txt")

os.remove("T10.txt")

os.remove("T11.txt")

os.remove("T12.txt")

os.remove("T13.txt")

os.remove("T14.txt")

os.remove("T15.txt")

os.remove("T16.txt")

os.remove("T17.txt")

os.remove("T18.txt")

os.remove("T19.txt")

os.remove("T20.txt")

os.remove("T21.txt")

os.remove("T22.txt")

os.remove("T23.txt")

os.remove("T24.txt")

os.remove("T25.txt")

os.remove("T26.txt")

os.remove("T30.txt")

os.remove("TT1.txt")

os.remove("TT2.txt")

os.remove("TT4.txt")

os.remove("TT5.txt")

os.remove("TT6.txt")

os.remove("TT7.txt")

os.remove("TT8.txt")

os.remove("TT9.txt")

os.remove("TT10.txt")

os.remove("TT11.txt")

os.remove("TT12.txt")

os.remove("TT13.txt")

os.remove("TT14.txt")

os.remove("TT15.txt")

os.remove("TT16.txt")

os.remove("TT17.txt")

os.remove("TT18.txt")

os.remove("TT19.txt")

os.remove("TT20.txt")

os.remove("TT21.txt")

os.remove("TT22.txt")

os.remove("TT23.txt")

os.remove("TT24.txt")

os.remove("TT25.txt")

os.remove("TT26.txt")

os.remove("TT30.txt")

print("任务运行完毕")
