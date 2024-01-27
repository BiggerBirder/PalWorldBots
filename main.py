import asyncio
import traceback

from process_operations import monitor_process_memory, terminate_process_by_name
from kookcommunication import get_guild_list, create_message, restart_msg
import time
import subprocess
import kookvoice
import json
import os


def open_file(path: str):
    # 打开配置文件
    with open(path, 'r', encoding='utf-8') as f:
        tmp = json.load(f)
    return tmp


current_working_directory = os.getcwd()
config = open_file(current_working_directory + r'\config\config.json')

token = config['token']
text_channel_id = config['text_channel_id']
voice_channel_id = config['voice_channel_id']
guild_id = config['guild_id']
server_process_name = config['server_process_name']
server_path = config['server_path']
backup_batch_path = config['backup_batch_path']


async def invoke_5minutes(music_path_or_link, guild_id, voice_channel_id):
    player = kookvoice.Player(guild_id, voice_channel_id, token)
    player.add_music(music_path_or_link)
    task = asyncio.create_task(kookvoice.run())
    await task


async def reboot_server(mem_msg):
    response = create_message(token,
                              restart_msg(mem_msg['memory_usage'], mem_msg['memory_percent'], mem_msg['total_percent'],
                                          5),
                              guild_id, text_channel_id)

    # 备份与游戏服务器文件
    subprocess.run([backup_batch_path], shell=True)
    time.sleep(10)
    # 5分钟后重启
    task = asyncio.create_task(invoke_5minutes(config["five_minutes_voice"], guild_id, voice_channel_id))
    await asyncio.sleep(4*60)
    try:
        task.cancel()
    except:
        print(traceback.format_exc())
    task = asyncio.create_task(invoke_5minutes(config["one_minute_voice"], guild_id, voice_channel_id))
    await asyncio.sleep(60)
    os.system("shutdown -t 0 -r -f")

async def restart_process(mem_msg):
    response = create_message(token,
                              restart_msg(mem_msg['memory_usage'], mem_msg['memory_percent'], mem_msg['total_percent'],
                                          5),
                              guild_id, text_channel_id)
    # 语音通知
    task = asyncio.create_task(invoke_5minutes(config["five_minutes_voice"], guild_id, voice_channel_id))
    await asyncio.sleep(5)
    # 备份与游戏服务器文件
    subprocess.run([backup_batch_path], shell=True)
    # 5分钟后重启
    time.sleep(4*60)
    try:
        task.cancel()
    except:
        print(traceback.format_exc())
    task = asyncio.create_task(invoke_5minutes(config["one_minute_voice"], guild_id, voice_channel_id))
    await asyncio.sleep(60)
    # 结束游戏服务器
    terminate_process_by_name(server_process_name)
    # 启动游戏服务器
    run_PalWorld(['start', server_path, '-useperfthreads', '-NoAsyncLoadingThread', '-UseMultithreadForDS'])
    try:
        task.cancel()
    except:
        print(traceback.format_exc())

def run_PalWorld(args):
    subprocess.run(args, shell=True)
    response = create_message(token,"游戏服务器启动了！快来玩！", guild_id, text_channel_id)


async def invoke_listener():
    kook_info = get_guild_list(token)
    guild_data = kook_info['data']
    guild_data_items = guild_data['items']
    name_id_list = [(item['name'], item['id'], item['default_channel_id']) for item in guild_data_items]
    for name, id, default_channel_id in name_id_list:
        guild_name_id = f"名称：{name}，公会ID：{id}，默认频道ID：{default_channel_id}"
        print(guild_name_id)
    response = create_message(token, "自动重启监听程序成功启动。", guild_id, text_channel_id)
    while True:
        mem_msg = monitor_process_memory(server_process_name)
        if mem_msg is None:
            # 如果没启动服务器，启动服务器
            run_PalWorld(['start', server_path, '-useperfthreads', '-NoAsyncLoadingThread', '-UseMultithreadForDS'])
            print("正在启动 " + server_process_name)
            await asyncio.sleep(10)
        else:
            if mem_msg['total_percent'] > 90:
                # 总系统内存占用超过阈值
                await reboot_server(mem_msg)

            elif mem_msg['memory_percent'] > 80:
                await restart_process(mem_msg)
                # 游戏服务器最大重启间隔时间1个小时
                time.sleep(60 * 60)
            else:
                print(
                    f"游戏进程的内存使用为{mem_msg['memory_usage']}MB，总服务器的内存使用率为{mem_msg['total_percent']}%，不超过90%，继续运行")
                if time.strftime("%M") == "30":
                    # 每小时备份一次服务器
                    subprocess.run([backup_batch_path], shell=True)
                time.sleep(60)


def main():
    '''
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(invoke_listener())
    loop.close()
    '''
    asyncio.run(invoke_listener())


# 调用主函数
if __name__ == "__main__":
    main()
