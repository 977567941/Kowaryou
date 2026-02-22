import json
import base64
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from typing import Optional

INPUT_FILE = "待解密.txt"
OUTPUT_FILE = "解密.json"

def read_input_file(file_path: str) -> tuple[Optional[str], Optional[str]]:
    """读取待解密.txt，提取链接和密钥"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        if len(lines) < 2:
            print("❌ 待解密.txt格式错误：需包含一行链接和一行密钥")
            return None, None
      
        link_pattern = re.compile(r'https?://[^\s]+')
        link_match = link_pattern.search(lines[0])
        link = link_match.group() if link_match else None
        if not link:
            print("❌ 未从第一行提取到有效链接")
            return None, None
        
        key = lines[1]
        if len(key) != 16:
            print(f"⚠️  密钥长度非16位（当前{len(key)}位），AES-128要求密钥必须16位")
            return None, None
        return link, key
    except Exception as e:
        print(f"❌ 读取文件失败：{str(e)}")
        return None, None

def fetch_encrypted_data(link: str) -> Optional[bytes]:
    """从链接获取加密数据（base64编码的data字段）"""
    try:
        import urllib.request
        import ssl
    
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
  
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36'
        }
        req = urllib.request.Request(link, headers=headers)
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
    
        json_data = json.loads(content)
        encrypted_b64 = json_data.get('data')
        if not encrypted_b64:
            print("❌ 响应中未找到'data'字段")
            return None
    
        return base64.b64decode(encrypted_b64)
    except json.JSONDecodeError:
        print("❌ 响应内容不是合法JSON")
        return None
    except Exception as e:
        print(f"❌ 获取加密数据失败：{str(e)[:50]}")
        return None

def aes_cbc_decrypt(ciphertext: bytes, key: str) -> Optional[str]:
    """AES-CBC解密（IV=密钥，PKCS7填充）"""
    try:
        key_bytes = key.encode('latin-1')
        iv_bytes = key_bytes 
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
   
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
        return plaintext.decode('utf-8')
    except Exception as e:
        print(f"❌ 解密失败：{str(e)}")
        return None

def save_decrypted_result(plaintext: str, output_file: str):
    """保存解密结果到JSON文件（自动格式化）"""
    try:
        
        try:
            json_data = json.loads(plaintext)
        except:
            
            json_data = {"decrypted_data": plaintext, "data_type": "text"}
   
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 解密结果已保存至：{output_file}")
  
        preview = json.dumps(json_data, ensure_ascii=False, indent=2)
        print("\n📋 解密结果预览（前500字符）：")
        print(preview[:500] + "..." if len(preview) > 500 else preview)
    except Exception as e:
        print(f"❌ 保存结果失败：{str(e)}")

def main():
    print("="*60)
    print("🚀 AES链接解密工具（简化版）")
    print("="*60)
    

    print(f"\n🔍 读取文件：{INPUT_FILE}")
    link, key = read_input_file(INPUT_FILE)
    if not link or not key:
        return
    print(f"✅ 提取链接：{link}")
    print(f"✅ 提取密钥：{key}")
   
    print(f"\n🌐 从链接获取加密数据...")
    ciphertext = fetch_encrypted_data(link)
    if not ciphertext:
        return
    print(f"✅ 获取加密数据成功（{len(ciphertext)}字节）")
    
    print(f"\n🔓 执行AES-CBC解密...")
    plaintext = aes_cbc_decrypt(ciphertext, key)
    if not plaintext:
        return
    print(f"✅ 解密成功！")
    
    print(f"\n💾 保存解密结果...")
    save_decrypted_result(plaintext, OUTPUT_FILE)
    
    print("\n" + "="*60)
    print("🎉 解密流程完成！")
    print("="*60)

if __name__ == "__main__":
    main()
