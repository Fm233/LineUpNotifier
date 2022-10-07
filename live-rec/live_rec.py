from Live import BiliBiliLive
import os
import time
import re
import urllib3
import subprocess as sp
import argparse
import aiohttp
import asyncio
from async_timeout import timeout
import sleep

urllib3.disable_warnings()

proxies = {"http": None, "https": None}
c_filename = os.path.join(os.getcwd(), 'recording', 'rec.mkv')
interval = 10


class BiliBiliLiveRecorder(BiliBiliLive):

    def __init__(self, room_id, session: aiohttp.ClientSession):
        super().__init__(room_id, session)

    async def check(self):
        while True:

            sleep.sleep_until_enabled()

            try:
                room_info = await self.get_room_info()
                print("[Info] 成功获取房间信息！")
                if room_info['status']:
                    print(self.room_id, room_info['roomname'])
                else:
                    print(self.room_id, '等待开播')
                    raise Exception("未开播！")
                print("[Info] 正在获取直播链接……")
                urls = await self.get_live_urls()
                break
            except Exception as e:
                print(self.room_id, 'Error:' + str(e))
            print(f'[Info] {interval}秒后重试获取链接！')
            time.sleep(interval)
        return urls

    async def record(self, record_url, output_filename):
        try:
            print(self.room_id, '√ 正在录制...' + self.room_id)
            headers = dict()
            headers['Accept-Encoding'] = 'identity'
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
            headers['Referer'] = re.findall(
                r'(https://.*\/).*\.flv',
                record_url)[0]
            async with self.session.get(record_url, headers=headers) as resp:

                # 手动 async for
                iter = resp.content.iter_chunked(1024)
                iter.__aiter__()
                running = True
                while running:
                    try:
                        # 增加流读取的 Timeout 机制
                        async with timeout(10):
                            chunk = await iter.__anext__()
                    except:
                        running = False
                    else:
                        pipe.stdin.write(chunk)

        except Exception as e:
            print(self.room_id, 'Error while recording:' + str(e))
            raise e

    async def run(self):
        try:
            print("[Info] 开始检查直播链接……")
            urls = await self.check()
            print("[Info] 成功获取直播链接！")
            await self.record(urls[0], c_filename)
        except Exception as e:
            print(self.room_id,
                  'Error while checking or recording:' + str(e))
            raise e


async def main():
    global pipe

    # 输入参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--room', type=int, default=25062334,
                        help='bilibili room id')
    opt = parser.parse_args()

    # 直播管道输出
    command = ['ffmpeg',
               '-y',
               '-i', '-',
               '-an',
               '-c:v', 'copy',
               '-r', '30',
               '-f', 'rtsp',
               '-rtsp_transport', 'tcp',
               'rtsp://rtsp-server:8554/1']

    while True:

        sleep.sleep_until_enabled()

        try:
            pipe = sp.Popen(command, stdin=sp.PIPE)

            print("[Info] 管道已打开！")
            async with aiohttp.ClientSession() as session:
                await BiliBiliLiveRecorder(opt.room, session).run()
        except Exception as e:
            print(f"[Error] {e}")

        print(f'[Info] {interval}秒后重试打开管道！')
        time.sleep(interval)


if __name__ == '__main__':
    asyncio.run(main())
