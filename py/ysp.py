import os
import time
import requests
from grpc_tools import protoc
import sys

# ==========================================
# 1. 精简后的 Proto 协议
# 仅保留 python 逻辑中实际访问的字段
# ==========================================
PROTO_CONTENT = """
syntax = "proto3";
package ysp;

message ApiResponse {
    int32 code = 1;
    DataBody data = 2;
}

message DataBody {
    ChannelContainer body = 2;
}

message ChannelContainer {
    repeated Channel channels = 15;
}

message Channel {
    bytes name = 2;             // 频道名
    bytes pid = 4;              // PID
    bytes vid = 6;              // VID
    int32 tag_7 = 7;            // 付费标记位
    bytes logo_large = 13; // 台标
    map<int32, ExtraInfo> extra = 16; // 权限 Map
}

message ExtraInfo {
    bytes id = 1;               // "30002": VIP 等 ID
}
"""


def setup_proto():
    """动态生成并编译"""
    work_dir = os.path.dirname(os.path.abspath(__file__))
    proto_path = os.path.join(work_dir, "ysp_core.proto")

    # 写入 Proto 文件
    with open(proto_path, "w", encoding="utf-8") as f:
        f.write(PROTO_CONTENT)

    # 编译 Proto
    protoc.main(['', f'-I{work_dir}', f'--python_out={work_dir}', proto_path])

    # 动态导入
    if work_dir not in sys.path:
        sys.path.append(work_dir)

    import ysp_core_pb2
    return ysp_core_pb2


# ==========================================
# 2. 核心请求与解析逻辑
# ==========================================
def run_task():
    try:
        pb2 = setup_proto()
    except ImportError:
        print("[!] 无法加载生成的 Proto 模块，请检查环境或 grpc_tools 安装。")
        return

    # 这里的 Timestamp 实际上对结果影响不大，但保留原逻辑
    url = f"https://capi.yangshipin.cn/api/oms/pc/page/PG00000004?{int(time.time() * 1000)}"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        'Referer': "https://www.yangshipin.cn/",
        'Origin': "https://www.yangshipin.cn",
        'Accept': 'application/x-protobuf, */*'
    }

    print(f"[*] 正在请求数据 (Bytes Mode)...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # 解析数据
        api_res = pb2.ApiResponse()
        api_res.ParseFromString(response.content)

        # 辅助函数：bytes 转 string
        def b2s(b):
            return b.decode('utf-8', errors='ignore') if isinstance(b, bytes) else str(b)

        print(f"[*] 解析成功 | Code: {api_res.code}")
        print("=" * 95)
        print(f"{'频道名称':<20} | {'PID (Tag 4)':<12} | {'VID (Tag 6)':<12} | 台标 (Tag 13)")
        print("-" * 95)

        # 遍历解析结果
        if not api_res.data.body.channels:
            print("[!] 未找到频道数据，可能结构已变更或 Proto 定义不匹配。")

        for ch in api_res.data.body.channels:
            # --- 数据提取 ---
            name = b2s(ch.name)
            vid = b2s(ch.vid)
            pid = b2s(ch.pid)
            logo = b2s(ch.logo_large)

            # 1. 提取 Extra Map 里的权限 ID
            # 注意：map 的 value 是 ExtraInfo message
            privilege_ids = [b2s(info.id) for info in ch.extra.values()]

            # 2. 权限逻辑判断
            tag_name = ""
            if "30002" in privilege_ids:
                tag_name = "(VIP)"
            elif "30001" in privilege_ids:
                tag_name = "(限免)"
            elif ch.tag_7 == 1:
                # 兜底逻辑
                if any(x in name for x in ["剧场", "怀旧"]):
                    tag_name = "(限免)"
                else:
                    tag_name = "(VIP)"

            # 输出
            print(f"{name + tag_name:<24} | {pid:<12} | {vid:<12} | {logo.replace('?imageMogr2/format/webp','')}")

    except requests.exceptions.RequestException as e:
        print(f"[!] 网络请求错误: {e}")
    except Exception as e:
        print(f"[!] 解析或逻辑错误: {e}")
        # 调试用：如果出错，打印一下原始数据的前50个字节
        if 'response' in locals():
            print(f"DEBUG: Head Hex: {response.content[:50].hex()}")


if __name__ == "__main__":
    run_task()