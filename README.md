# 脚本集

存放各类实用小脚本。


### TUNET.sh

使用 `curl` 模拟清华校园网登陆。


###  weechat_bot2human.py

用于 WeeChat IRC 客户端，将各类 bot 转发的消息(例如 Fishroom) 中的 nickname 提取出来，替换 bot 名字。
使用方法:
 - 将 [weechat_bot2human.py](weechat_bot2human.py) 放到 `~/.weechat/python/autoload` 中
 - 设置需要替换的 bot 名，多个 bot 用空格分割，例如 `/set plugins.var.python.bot2human.bot_nicks teleboto tg2arch`
