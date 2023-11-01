#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
File: tg_sign.py(telegram签到)
Author: Zerolouis
cron: 0 13 10 * * *
new Env('自动telegram签到');
Update: 2023/9/5
"""
import asyncio
import os
import random

from telethon import TelegramClient

import notify

api_id = eval(os.environ['tg_api_id'])
api_hash = os.environ['tg_api_hash']
channel_urls = os.environ['tg_channel_urls'].split(',')
channel_signs = os.environ['tg_channel_signs'].split(',')
send_dir = dict(zip(channel_urls, channel_signs))

tg_log = "Tg 签到日志: \n"

def get_client():
    return TelegramClient('anon', api_id, api_hash)


def get_chat_message(channel_url):
    messages = client.iter_messages(channel_url, limit=1)
    for message in messages:
        print(message.text, end='\n')


async def send_message(channel_url: str, text: str):
    await client.send_message(channel_url, text)


async def read_message(channel_url: str):
    await client.send_read_acknowledge(channel_url)


async def auto_check(channel_url: str, text: str):
    try:
        await send_message(channel_url, text)
        await asyncio.sleep(random.randint(1, 3))
        await read_message(channel_url)
        log = "Done! Channel Id:" + channel_url.split('/')[-1] + "Text:" + text + "\n"
    except Exception as e:
        log = "Error! Channel Id:" + channel_url.split('/')[-1] + "Text:" + text + "Error:" + str(e) + "\n"
    print(log)
    return log


async def main(log: str = tg_log):
    for channel, message in send_dir.items():
        log += await auto_check(channel, message)
        await asyncio.sleep(random.randint(2, 5))
    print(log)
    notify.wecom_app("tg签到", log)


async def test():
    await client.send_message('me', 'Hello, myself!')
    notify.wecom_app("tg签到", "test")
    print("test")


if __name__ == '__main__':
    with get_client() as client:
        client.loop.run_until_complete(main())
        # client.loop.run_until_complete(test())
