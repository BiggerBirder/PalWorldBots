import requests
from urllib.parse import urlencode
from datetime import datetime, timedelta


# 定义处理请求的函数
def call_api(endpoint, token, method="GET", params=None, data=None):
    # 定义 API 接口的基础 URL
    api_base_url = "https://www.kookapp.cn"
    url = api_base_url + endpoint

    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }

    if method == "GET":
        if params is not None:
            query_string = urlencode(params)
            url += "?" + query_string
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    else:
        raise ValueError("Invalid HTTP method.")

    return response.json()


# 获取服务器信息
def get_guild_list(token, page=None, page_size=None, sort=None):
    endpoint = "/api/v3/guild/list"

    params = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size
    if sort is not None:
        params["sort"] = sort

    response = call_api(endpoint, token, method="GET", params=params)
    return response


# 发送信息 (guild_id:服务器id target_id：频道id)
def create_message(token, content, guild_id, channel_id):
    endpoint = "/api/v3/message/create"
    data = {
        "type": 1,
        "target_id": channel_id,
        "content": content,
        "guild_id": guild_id
    }
    response = call_api(endpoint, token, method="POST", data=data)
    return response


def restart_msg(memory_usage_mb, memory_percent, total_percent, interval_minutes=5):
    current_time = datetime.now()
    next_restart_time = current_time + timedelta(minutes=interval_minutes)
    formatted_current_time = str(current_time)[:19]
    formatted_next_restart_time = str(next_restart_time)[:19]
    full_msg_format = f"@在线成员 {formatted_current_time}\n当前游戏进程已占用{memory_percent}%，用量{memory_usage_mb}MB，服务器总体内存使用比例{total_percent}%。正在重启中...\n服务器将于{formatted_next_restart_time}重启。"
    return full_msg_format
