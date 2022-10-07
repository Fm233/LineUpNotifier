from nonebot import on_command, CommandSession
import detect_data
import localize


# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('count', permission=lambda sender: sender.is_superuser)
async def send_num(session: CommandSession):
    tlb, tub, res, cnt, img_id = detect_data.get()
    if cnt == 0:
        await session.send('cnt = 0')
        return
    await session.send(localize.send(tlb, tub, res, cnt))
    await session.send(localize.send_img(img_id))
