import nonebot
import detect_data
import localize
import sleep
from secret import *
from nonebot import NoneBot
from aiocqhttp.exceptions import Error as CQHttpError

# Configuration Area

timeout_cycle = 60  # Alert cooldown will be interval * timeout_cycle
interval = 10  # Detect interval
qq_group = secret_qq_group
qq_debugger = secret_qq_debugger
num_threshold = 10  # Send message when there are less people.

# Temp variables

cooldown = 0


@nonebot.scheduler.scheduled_job('interval', seconds=interval)
async def _():
    global cooldown

    if not sleep.active():
        return

    # Get data and bot
    tlb, tub, res, cnt, img_id = detect_data.get()
    bot = nonebot.get_bot()
    print('[Info] 判断是否发送消息……')

    # Maintain cooldown
    if cooldown > 0:
        cooldown -= 1
    if cooldown < 0:
        cooldown = 0

    # Error block
    if detect_data.not_timely(tub):
        print('[Error] 消息失去时效性！')
        return
    if res <= 0:
        print('[Error] 结果等于或小于0！')
        return
    if cnt <= 5:
        print('[Error] 缓冲区样本少于或等于5个！')
        return

    # Send if not in cooldown
    if res < num_threshold and cooldown == 0:

        # Get message to send
        msg = localize.send(tlb, tub, res, cnt)
        img = localize.send_img(img_id)

        # Try to send message
        try:
            await send_group(bot, msg, img)
            cooldown += timeout_cycle
        except CQHttpError:
            print("[ERROR] 网络有问题，无法发送消息！")
            pass


async def send_group(bot: NoneBot, msg, img):
    await bot.send_group_msg(group_id=qq_group, message=msg)
    await bot.send_group_msg(group_id=qq_group, message=img)
