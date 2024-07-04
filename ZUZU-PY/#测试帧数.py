

#测速并记录读取的帧数和读取时间


import cv2
import time

# 用于存储已经测试过的IP和结果，以及测试时间和帧数
# 'ok' 表示成功，'tested' 表示已测试但可能未成功
tested_ips = {}

# 打开文件，并设置编码为utf-8
with open('M临时测速.txt', 'r', encoding='utf-8') as file:
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
            
            # 初始化开始时间和帧数计数器
            start_time = time.time()
            frame_count = 0
            
            # 尝试读取视频帧
            while frame_count < 9999 and (time.time() - start_time) < 10:  # 超时时间
                ret, frame = cap.read()
                if not ret:  # 检查是否成功读取到帧
                    break  # 如果没有读取到帧，则跳出循环
                frame_count += 1  # 成功读取一帧，计数器加1

            # 记录读取帧的总时间和总帧数
            end_time = time.time()
            total_time = end_time - start_time

            # 根据测试结果更新字典，并添加测试时间和帧数
            if frame_count > 2:  # 限定合格IP判定的帧数
                tested_ips[ip_part] = {'status': 'ok', 'frames': frame_count, 'time': total_time}
            else:
                # 如果没有读取到足够多的帧，则标记为已测试
                tested_ips[ip_part] = {'status': 'tested', 'frames': frame_count, 'time': total_time}

            # 释放VideoCapture对象
            cap.release()

# 测试结束后，将包含ok的IP的channel写入新文件，并追加测试时间和帧数
with open('M测速结果.txt', 'w', encoding='utf-8') as file:
    with open('M临时测速.txt', 'r', encoding='utf-8') as input_file:
        for line in input_file:
            # 检查行中是否包含1个逗号，以确保是channel
            if line.count(',') == 1:
                # 截取IP部分（这里我们假设IP在第一个逗号之后，直到'rtp'或行尾）
                ip_start = line.find(',') + 1
                rtp_pos = line.find('rtp')
                if rtp_pos != -1:
                    ip_part = line[ip_start:rtp_pos].strip()
                else:
                    ip_part = line[ip_start:].strip()  # 如果没有'rtp'，则取到行尾

                # 检查IP是否测试成功
                if ip_part in tested_ips and tested_ips[ip_part]['status'] == 'ok':
                    # 追加测试结果到输出文件的每一行末尾
                    result_line = line.strip() + f"速度{tested_ips[ip_part]['frames']}"
                    file.write(result_line + '\n')
