import psutil

def get_total_memory_usage_percent():
    return psutil.virtual_memory().percent
# 通过进程名查找进程
def find_process_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc
    return None


# 获取进程的内存信息（以MB为单位）
def get_process_memory_info(process):
    memory_info = process.memory_info()
    memory_usage = memory_info.rss / (1024 * 1024)  # 内存占用转换为MB单位
    memory_usage_mb = round(memory_usage, 2)  #
    memory_percent = round(process.memory_percent(), 2)
    return {
        'pid': process.pid,
        'name': process.name(),
        'memory_usage': memory_usage_mb,
        'memory_percent': memory_percent,
        'total_percent': get_total_memory_usage_percent()
    }


# 监控特定进程的内存信息
def monitor_process_memory(process_name):
    while True:
        process = find_process_by_name(process_name)
        if process is None:
            print("未找到进程：", process_name)
            return None
        else:
            memory_info = get_process_memory_info(process)
            memory_info_format = {
                'pid': memory_info['pid'],
                'name': memory_info['name'],
                'memory_usage': memory_info['memory_usage'],
                'memory_percent': memory_info['memory_percent'],
                'total_percent': memory_info['total_percent']
            }
            return memory_info_format


def terminate_process_by_name(process_name):
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            proc.terminate()

