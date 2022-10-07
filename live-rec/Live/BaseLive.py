import aiohttp


class BaseLive:
    def __init__(self, session: aiohttp.ClientSession):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9',
            'sec-ch-ua': '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53'
        }
        self.session = session
        # self.session.trust_env = False
        self.site_name = ''
        self.site_domain = ''

    async def common_request(self, method, url, params=None, data=None) -> aiohttp.ClientResponse:
        connection = None
        if method == 'GET':
            connection = await self.session.get(
                url, headers=self.headers, params=params, timeout=10)
        if method == 'POST':
            connection = await self.session.post(
                url, headers=self.headers, params=params, data=data, timeout=10)
        return connection

    def get_room_info(self):
        pass

    def get_live_urls(self):
        pass
