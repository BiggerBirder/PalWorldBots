from khl import Bot, Message, EventTypes, PublicMessage
from kookcommunication import create_message
from process_operations import monitor_process_memory
import main
import json

def open_file(path: str):
    # 打开配置文件
    with open(path, 'r', encoding='utf-8') as f:
        tmp = json.load(f)
    return tmp


config = open_file(r'./config/config.json')

token = config['token']
text_channel_id = config['text_channel_id']
voice_channel_id = config['voice_channel_id']
guild_id = config['guild_id']
server_process_name = config['server_process_name']
interval_minutes = config['interval_minutes']  # minutes
server_path = config['server_path']
backup_batch_path = config['backup_batch_path']

bot = Bot(token=token)

create_message(token,"Allygei小机器人启动了！", guild_id, text_channel_id)
print("机器人启动")


@bot.command(name="查看内存")
async def check_memory(msg:Message):
    if msg.ctx.channel.id == text_channel_id:
        mem_msg = monitor_process_memory(server_process_name)
        ch = await bot.client.fetch_public_channel(text_channel_id)
        ret = await ch.send(
            f"游戏进程的内存使用为{mem_msg['memory_usage']}MB，总服务器的内存使用率为{mem_msg['total_percent']}%")
        print(f"ch.send | msg_id {ret['msg_id']}")


@bot.command(name="重启游戏服务器！")
async def restart_process(msg:Message):
    if msg.ctx.channel.id == text_channel_id:
        mem_msg = monitor_process_memory(server_process_name)
        ch = await bot.client.fetch_public_channel(text_channel_id)
        ret = await ch.send(
            f"游戏进程的内存使用为{mem_msg['memory_usage']}MB，总服务器的内存使用率为{mem_msg['total_percent']}%。\n5分钟后重启游戏服务器！（不是重启整个服务器）")
        await main.restart_process(mem_msg)
        print(f"ch.send | msg_id {ret['msg_id']}")


@bot.command(name="重启整个服务器！")
async def reboot_server(msg:Message):
    if msg.ctx.channel.id == text_channel_id:
        mem_msg = monitor_process_memory(server_process_name)
        ch = await bot.client.fetch_public_channel(text_channel_id)
        ret = await ch.send(
            f"游戏进程的内存使用为{mem_msg['memory_usage']}MB，总服务器的内存使用率为{mem_msg['total_percent']}%。\n5分钟后重启整个服务器！（效果更好）")
        await main.reboot_server(mem_msg)
        print(f"ch.send | msg_id {ret['msg_id']}")


if __name__ == "__main__":
    bot.run()