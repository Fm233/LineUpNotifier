from .BaseLive import BaseLive
import aiohttp


class BiliBiliLive(BaseLive):
    def __init__(self, room_id, session: aiohttp.ClientSession):
        super().__init__(session)
        self.room_id = room_id
        self.site_name = 'BiliBili'
        self.site_domain = 'live.bilibili.com'

    async def get_room_info(self):
        data = {}
        room_info_url = 'https://api.live.bilibili.com/room/v1/Room/get_info'
        user_info_url = 'https://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room'

        print("sending room info request...")
        resp = await self.common_request('GET', room_info_url, {
            'room_id': self.room_id
        })
        response = await resp.json()
        if response['msg'] == 'ok':
            data['roomname'] = response['data']['title']
            data['site_name'] = self.site_name
            data['site_domain'] = self.site_domain
            data['status'] = response['data']['live_status'] == 1
        self.room_id = str(response['data']['room_id'])

        print("sending host name request...")
        resp = await self.common_request('GET', user_info_url, {
            'roomid': self.room_id
        })
        response = await resp.json()
        data['hostname'] = response['data']['info']['uname']
        print("info get!")
        return data

    async def get_live_urls(self):
        live_urls = []
        url = 'https://api.live.bilibili.com/room/v1/Room/playUrl'

        print("send stream info request...")
        resp = await self.common_request('GET', url, {
            'cid': self.room_id,
            'otype': 'json',
            'quality': 0,
            'platform': 'web'
        })
        stream_info = await resp.json()
        best_quality = stream_info['data']['accept_quality'][0][0]

        print("send stream url request...")
        resp = await self.common_request(
            'GET', url, {
                'cid': self.room_id,
                'otype': 'json',
                'quality': best_quality,
                'platform': 'web'
            })
        stream_info = await resp.json()
        for durl in stream_info['data']['durl']:
            live_urls.append(durl['url'])
        print("live urls get!")
        return live_urls
