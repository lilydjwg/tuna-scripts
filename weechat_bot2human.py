# -*- coding:utf-8 -*-
# Bot2Human
#
# Replaces messages from bots to humans
# typically used in channels that are connected with other IMs using bots
#
# For example, if a bot send messages from XMPP is like `[nick] content`,
# weechat would show `bot | [nick] content` which looks bad; this script
# make weecaht display `nick | content` so that the messages looks like
# normal IRC message
#
# Options
#
#   plugins.var.python.bot2human.bot_nicks
#       space seperated nicknames to forwarding bots
#       example: teleboto toxsync tg2arch
#
#   plugins.var.python.nick_content_re.X
#       X is a 0-2 number. This options specifies regex to match nickname
#       and content. Default regexes are r'\[(?P<nick>.+?)\] (?P<text>.*)',
#       r'\((?P<nick>.+?)\) (?P<text>.*)', and r'<(?P<nick>.+?)> (?P<text>.*)'
#

# Changelog:
#
# 0.1.1: Bug Fixes
# 0.1: Initial Release
#

import weechat as w
import re

SCRIPT_NAME = "bot2human"
SCRIPT_AUTHOR = "Justin Wong & Hex Chain"
SCRIPT_DESC = "Replace IRC message nicknames with regex match from chat text"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPLv3"

DEFAULTS = {
    'nick_content_re.0': r'\[(?P<nick>.+?)\] (?P<text>.*)',
    'nick_content_re.1': r'\((?P<nick>.+?)\) (?P<text>.*)',
    'nick_content_re.2': r'<(?P<nick>.+?)> (?P<text>.*)',
    'bot_nicks': "",
}

CONFIG = {
    'nick_content_res': [],
    'bot_nicks': [],
}


def parse_config():

    for option, default in DEFAULTS.items():
        # print(option, w.config_get_plugin(option))
        if not w.config_is_set_plugin(option):
            w.config_set_plugin(option, default)

    CONFIG['bot_nicks'] = w.config_get_plugin('bot_nicks').split(' ')
    for option in DEFAULTS:
        if option.startswith("nick_content_re"):
            CONFIG['nick_content_res'].append(
                re.compile(w.config_get_plugin(option))
            )


def config_cb(data, option, value):
    parse_config()

    return w.WEECHAT_RC_OK


def msg_cb(data, modifier, modifier_data, string):
    # w.prnt("blue", "test_msg_cb " + string)
    parsed = w.info_get_hashtable("irc_message_parse", {'message': string})
    # w.prnt("", "%s" % parsed)

    matched = False
    for bot in CONFIG['bot_nicks']:
        # w.prnt("", "%s, %s" % (parsed["nick"], bot))
        if parsed['nick'] == bot:
            for r in CONFIG['nick_content_res']:
                m = r.match(parsed['text'])
                if not m:
                    continue
                nick, text = m.group('nick'), m.group('text')
                nick = re.sub(r'\s', '_', nick)
                parsed['host'] = parsed['host'].replace(bot, nick)
                parsed['text'] = text
                matched = True
            if matched:
                break
    else:
        return string

    return ":{host} {command} {channel} {text}".format(**parsed)


if __name__ == '__main__':
    w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
               SCRIPT_DESC, "", "")

    parse_config()

    w.hook_modifier("irc_in_privmsg", "msg_cb", "")
    w.hook_modifier("plugins.var.python."+SCRIPT_NAME+".*", "config_cb", "")

# vim: ts=4 sw=4 sts=4 expandtab
