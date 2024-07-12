import os
import requests
import re
import base64
import cv2
import datetime
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse

#enter
files = os.listdir('rtp')

files_name = []

#enter
for file in files:
    name, extension = os.path.splitext(file)
    files_name.append(name)

#enter
provinces_isps = [name for name in files_name if name.count('_') == 1]

#enter
print(f"enter：{provinces_isps}enter") 

keywords = []

for province_isp in provinces_isps:
    #enter
    try:
        with open(f'rtp/{province_isp}.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines if line.strip()]
        #enter
        if lines:
            first_line = lines[0]
            if "rtp://" in first_line:
                mcast = first_line.split("rtp://")[1].split(" ")[0]
                keywords.append(province_isp + "_" + mcast)
    except FileNotFoundError:
    #enter
        print(f"enter '{province_isp}.txt' enter.")

for keyword in keywords:
    province, isp, mcast = keyword.split("_")
    #enter
    #enter
    if province == "北京" and isp == "联通":
        isp_en = "cucc"
        org = "China Unicom Beijing Province Network"
    elif isp == "联通":
        isp_en = "cucc"
        org = "CHINA UNICOM China169 Backbone"
    elif isp == "电信":
        org = "Chinanet"
        isp_en = "ctcc"
    elif isp == "移动":
        org == "China Mobile communications corporation"
        isp_en = "cmcc"
        
#    else:
#        org = ""

    current_time = datetime.now()
    timeout_cnt = 0
    result_urls = set() 
    while len(result_urls) == 0 and timeout_cnt <= 5:
        try:
            search_url = 'https://fofa.info/result?qbase64='
            search_txt = f'\"udpxy\" && country=\"CN\" && region=\"{province}\" && org=\"{org}\"'
                #enter
            bytes_string = search_txt.encode('utf-8')
                #enter
            search_txt = base64.b64encode(bytes_string).decode('utf-8')
            search_url += search_txt
            print(f"{current_time} enter : {province}{isp} ，enter : {search_url}")
            response = requests.get(search_url, timeout=5)
            #enter
            response.raise_for_status()
            #enter
            html_content = response.text
            #enter
            html_soup = BeautifulSoup(html_content, "html.parser")
            # print(f"{current_time} html_content:{html_content}")
            #enter
            #enter
            pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"
            urls_all = re.findall(pattern, html_content)
            #enter
            result_urls = set(urls_all)
            print(f"{current_time} result_urls:{result_urls}")

            valid_ips = []

            #enter
            for url in result_urls:
                video_url = url + "/rtp/" + mcast

                #enter
                cap = cv2.VideoCapture(video_url)

                #enter
                if not cap.isOpened():
                    print(f"{current_time} {video_url} enter")
                else:
                    #enter
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    print(f"{current_time} {video_url} enter{width}x{height}")
                    #enter
                    if width > 0 and height > 0:
                        valid_ips.append(url)
                    #enter
                    cap.release()
                    
            if valid_ips:
                #enter
                rtp_filename = f'rtp/{province}_{isp}.txt'
                with open(rtp_filename, 'r', encoding='utf-8') as file:
                    data = file.read()
                txt_filename = f'{province}{isp}.txt'
                with open(txt_filename, 'w') as new_file:
                    for url in valid_ips:
                        new_data = data.replace("rtp://", f"{url}/rtp/")
                        new_file.write(new_data)

                print(f'enter，enter{txt_filename}')

        except (requests.Timeout, requests.RequestException) as e:
            timeout_cnt += 1
            print(f"{current_time} [{province}]enter：{timeout_cnt}")
            if timeout_cnt <= 3:
                    #enter
                continue
            else:
                print(f"{current_time} enter[]，enter：{timeout_cnt} enter，enter")
print('enter！')
