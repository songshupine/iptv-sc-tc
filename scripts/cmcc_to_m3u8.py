import json
import re
import requests
from datetime import datetime, timezone, timedelta

def append_telecom_add_to_m3u8(udpxy_m3u8_file):
    """
    将 cmcc_add.m3u8 的内容追加到指定的 M3U8 文件末尾。
    
    :param udpxy_m3u8_file: generateUdpxyM3U8 生成的目标文件路径（如 'telecom.m3u8'）
    """
    
    add_file = "./public/home/cmcc_add.m3u8"
    
    try:
        with open(add_file, "r", encoding="utf-8") as f_add:
            extra_content = f_add.read()
        
        if not extra_content.strip():
            print(f"⚠️  {add_file} 为空，跳过追加。")
            return

        with open(udpxy_m3u8_file, "a", encoding="utf-8") as f_out:
            f_out.write("\n")
            f_out.write(extra_content.rstrip("\n") + "\n")
        
        print(f"✅ 已成功将 {add_file} 内容追加到 {udpxy_m3u8_file}")
    
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}")
    except Exception as e:
        print(f"⚠️ 追加过程中出错: {e}")

def clean_uuid_map(uuid_raw):
    """
    对 clean_uuid 进行特殊映射：
      ysten-cctv-1  -> cctv-1
      ysten-cctv-5  -> cctv-5
      ysten-cctv5plus -> hdcctv05plus
    其他保持不变。
    """
    cleaned = uuid_raw.removeprefix("ysten-") if uuid_raw.startswith("ysten-") else uuid_raw
    
    mapping = {
        "cctv-1": "cctv-1",
        "cctv-5": "cctv-5",
        "cctv5plus": "hdcctv05plus",
    }
    
    return mapping.get(cleaned, cleaned)

def process_channel_item(item, logo_url, catchup_source, upd_ip, group_map):
    """
    处理单个频道条目，返回 M3U8 格式的三行内容（KODIPROP、EXTINF、URL）。
    """
    uuid = item.get('uuid', 'N/A')
    channel_icon = item.get('channelIcon', '')
    channel_name = item.get('channelName', '未知频道')
    live_url = item.get('livePlayUrl', '')

    rtp_match = re.search(r'rtp://@?([^?]+)', str(live_url))
    rtp_base = rtp_match.group(1) if rtp_match else str(live_url)
    tvg_id_match = re.search(r'logo/(.+?)\.', channel_icon)
    tvg_id = tvg_id_match.group(1) if tvg_id_match else channel_name
    channel_name_clean = channel_name.replace("4K", "")

    tvg_id_upper = tvg_id.upper()
    channel_name_upper = channel_name.upper()
    group = next(
        (g for g, keywords in group_map.items() if any(kw in tvg_id_upper or kw in channel_name_upper for kw in keywords)),
        "其他"
    )

    clean_uuid = clean_uuid_map(uuid)
    catchup_source_new = catchup_source.replace("channel_uid", clean_uuid)

    lines = []
    lines.append('#KODIPROP:inputstream=inputstream.ffmpegdirect')
    lines.append(f'#EXTINF:-1 tvg-logo="{logo_url}{tvg_id}.png" tvg-id="{tvg_id}" tvg-name="{channel_name_clean}" catchup="default" catchup-days="5" catchup-source="{catchup_source_new}" group-title="{group}",{channel_name}')
    lines.append(upd_ip + rtp_base.split("rtp://")[-1])
    return lines

def extract_channels_to_text():
    input_filename = 'https://epg.gotonas.com/cmcc_channel.json'
    input_filename_b = 'https://epg.gotonas.com/cmcc_channel_b.json'
    output_filename = './public/home/cmcc.m3u8'
    epg_file = 'https://epg.gotonas.com/t.xml.gz'
    logo_url = 'https://tv.gotonas.com/logo/'
    catchup_source = 'http://zxhk.scmcc.sctv.com:8089/yst.lookback.scmobile.com/223.87.21.116:8080/ysten-business/lookback/channel_uid/${(b)yyyyMMddHHmmss}/${(e)yyyyMMddHHmmss}/1.m3u8'
    upd_ip = 'http://192.168.100.1:4022/udp/'
    group_map = {
        "CCTV": ["CCTV", "央视"],
        "卫视": ["卫视"],
        "四川": ["四川", "SC", "CD", "成都", "峨眉"]
    }

    # ========== 1. 读取主 JSON ==========
    try:
        response = requests.get(input_filename, timeout=10)
        response.raise_for_status()
        json_data = response.json()
        print(f"成功从网络加载主频道数据：{len(json_data)} 个频道。")
    except requests.RequestException as e:
        print(f"网络请求错误：{e}")
        return
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误：{e}")
        return

    # ========== 2. 读取备用 JSON ==========
    json_data_b = []
    try:
        response_b = requests.get(input_filename_b, timeout=10)
        response_b.raise_for_status()
        json_data_b = response_b.json()
        print(f"成功从网络加载备用频道数据：{len(json_data_b)} 个频道。")
    except requests.RequestException as e:
        print(f"⚠️ 备用频道网络请求错误（已跳过）：{e}")
    except json.JSONDecodeError as e:
        print(f"⚠️ 备用频道 JSON 解析错误（已跳过）：{e}")

    # ========== 3. 收集主文件所有 UUID（经 clean_uuid_map 处理后） ==========
    uuid_set_main = set()
    for item in json_data:
        uuid = item.get('uuid', '')
        if uuid:
            uuid_set_main.add(clean_uuid_map(uuid))

    # ========== 4. 过滤备用频道：UUID 不重复 且 livePlayUrl 以 rtp 或 @rtp 开头 ==========
    extra_channels = []
    skipped_uuid_dup = 0
    skipped_url = 0

    for item in json_data_b:
        uuid = item.get('uuid', '')
        clean_uuid = clean_uuid_map(uuid) if uuid else ''
        live_url = str(item.get('livePlayUrl', ''))

        # 条件1：UUID 不能在主文件中已存在
        if clean_uuid in uuid_set_main:
            skipped_uuid_dup += 1
            continue

        # 条件2：livePlayUrl 必须以 rtp 或 @rtp 开头
        if not (live_url.startswith("rtp") or live_url.startswith("@rtp")):
            skipped_url += 1
            continue

        extra_channels.append(item)
        # 加入已处理集合，防止备用文件自身 UUID 重复
        uuid_set_main.add(clean_uuid)

    print(f"备用频道过滤结果：共 {len(json_data_b)} 条 → 新增 {len(extra_channels)} 条（UUID重复跳过 {skipped_uuid_dup}，非rtp地址跳过 {skipped_url}）")

    # ========== 5. 按 index 排序 ==========
    try:
        json_data.sort(key=lambda x: int(x.get('index', 0)))
        print("主频道数据已按 Index 升序排序。")
    except ValueError as e:
        print(f"警告：主频道 Index 字段包含非数字内容，排序可能不准确。错误信息: {e}")

    try:
        extra_channels.sort(key=lambda x: int(x.get('index', 0)))
        if extra_channels:
            print("备用频道数据已按 Index 升序排序。")
    except ValueError as e:
        print(f"警告：备用频道 Index 字段包含非数字内容，排序可能不准确。错误信息: {e}")

    # ========== 6. 生成 M3U8 内容 ==========
    output_lines = []
    UTC8 = timezone(timedelta(hours=8))
    header = f'#EXTM3U name="四川移动IPTV - {datetime.now(UTC8).strftime("%Y-%m-%d %H:%M:%S")}" x-tvg-url="{epg_file}"'
    output_lines.append(header)

    # 处理主频道
    for item in json_data:
        output_lines.extend(process_channel_item(item, logo_url, catchup_source, upd_ip, group_map))

    # 处理备用频道（追加在主频道之后）
    for item in extra_channels:
        output_lines.extend(process_channel_item(item, logo_url, catchup_source, upd_ip, group_map))

    # ========== 7. 写入文件 ==========
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    append_telecom_add_to_m3u8(output_filename)

    print(f"成功生成提取文件：{output_filename}")
    print("\n预览前 5 行数据：")
    for i in range(min(5, len(output_lines))):
        print(output_lines[i])


if __name__ == '__main__':
    extract_channels_to_text()
