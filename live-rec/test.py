from Live import BiliBiliLive
import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        await BiliBiliLive(25062334, session).get_room_info()
        print('[Congrats] 可正常获取直播房间信息！')


if __name__ == '__main__':
    asyncio.run(main())
