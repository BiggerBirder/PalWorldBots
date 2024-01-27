# PalWorldBots

幻兽帕鲁自动化Kook机器人，自动监控内存使用，达到阈值自动重启服务器，也可手动。

# 感谢
参考了以下几个项目来做的机器人

[palworldrestartkook](https://github.com/wtfllix/palworldrestartkook/)

[simple-kook-voice](https://github.com/Edint386/simple-kook-voice)

[khl.py](https://github.com/TWT233/khl.py)

# 环境依赖
这个项目是基于windows系统开发的，用到了
- khl.py 
- ffmpeg
- urllib
- psutil

~~如果还有其他的跑的时候报错了就知道了~~

# 使用方法
把./config/config.json文件，对应的数据添加成自己的。
```json
{
    "token": "你的kook机器人token",
    "voice_channel_id": "希望机器人进入的语音频道id",
    "text_channel_id": "希望机器人收发消息的文字频道id",
    "guild_id": "kook服务器id",
    "five_minutes_voice": "五分钟提醒语音位置",
    "one_minute_voice": "一分钟提醒语音位置",
    "server_path": "游戏服务器位置",
    "server_process_name": "PalServer-Win64-Test-Cmd.exe",
    "backup_batch_path": "自动备份的bat文件路径"
}
```
运行main.py是自动监控服务器
运行kookbot.py是机器人可以手动查看内存使用和重启服务器
注意为了避免恶意指令或者误判，只有在text_channel_id里的指令才会执行。