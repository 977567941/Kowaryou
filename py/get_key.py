import os
import re
import base64
import threading
from queue import Queue
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

found = False
result_key = ""
result_plaintext = ""
progress_counter = 0
total_attempts = 0
lock = threading.Lock()


def extract_printable_strings(lib_path):
    try:
        with open(lib_path, 'rb') as f:
            content = f.read()
        pattern = b'[ -~]{16,}'
        matches = re.findall(pattern, content)
        unique_strings = list(set([match.decode('utf-8', errors='ignore') for match in matches]))
        return unique_strings
    except Exception as e:
        print(f"提取字符串时出错: {str(e)}")
        return []


def generate_16char_substrings(original):
    substrings = []
    if len(original) < 16:
        return substrings
    for i in range(len(original) - 15):
        substring = original[i:i + 16]
        substrings.append(substring)
    return substrings


def decrypt_aes_cbc(ciphertext, key):
    try:
        if len(key) != 16:
            return None
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv=key.encode('utf-8'))
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode('utf-8')
    except:
        return None


def worker(queue, ciphertext):
    global found, result_key, result_plaintext, progress_counter
    while not queue.empty() and not found:
        key = queue.get()
        plaintext = decrypt_aes_cbc(ciphertext, key)
        with lock:
            progress_counter += 1
            progress = (progress_counter / total_attempts) * 100
            print(f"\r处理进度: {progress:.2f}% | 已尝试: {progress_counter}/{total_attempts} | 当前密钥: {key}",
                  end='', flush=True)
        if plaintext:
            with lock:
                found = True
                result_key = key
                result_plaintext = plaintext
            print(f"\n找到有效密钥: {key}")
            break
        queue.task_done()

def main():
    global total_attempts, progress_counter
    try:
        with open('encrypt.txt', 'r') as f:
            encrypted_data = base64.b64decode(f.read().strip())
        print("成功读取加密文件")
    except Exception as e:
        print(f"读取加密文件失败: {str(e)}")
        return
    print("从libapp.so提取可打印字符串...")
    all_strings = extract_printable_strings('libapp.so')
    if not all_strings:
        print("未从libapp.so中找到任何足够长度的可打印字符串")
        return
    print(f"找到 {len(all_strings)} 个符合条件的字符串")
    print("生成16位候选密钥...")
    all_keys = []
    for s in all_strings:
        substrings = generate_16char_substrings(s)
        all_keys.extend(substrings)
    all_keys = list(set(all_keys))
    total_attempts = len(all_keys)
    print(f"生成 {total_attempts} 个候选密钥（去重后）")
    if total_attempts == 0:
        print("没有可用的候选密钥")
        return
    queue = Queue()
    for key in all_keys:
        queue.put(key)
    num_threads = min(os.cpu_count() * 2, 16, total_attempts)
    print(f"使用 {num_threads} 个线程进行破解...")
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(queue, encrypted_data))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    if found:
        with open('key.txt', 'w') as f:
            f.write(result_key)
        with open('decrypt.txt', 'w') as f:
            f.write(result_plaintext)
        print(f"\n尝试成功！")
        print(f"密钥已保存到 key.txt")
        print(f"解密结果已保存到 decrypt.txt")
    else:
        print("\n未能找到有效的密钥，解密失败")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"程序运行时间: {end_time - start_time:.2f} 秒")
