from datetime import datetime, timedelta
import requests


def get():
    '''Get time lower bound, time upper bound, averaged result and current buffer length.'''
    # Get from server
    try:
        resp = requests.get('http://nab-server:8000/avg/').json()
        tlb = datetime.strptime(resp['tlb'], '%Y-%m-%d %H:%M:%S')
        tub = datetime.strptime(resp['tub'], '%Y-%m-%d %H:%M:%S')
        s = resp['s']
        count = resp['count']
        img_id = resp['img_id']
        return tlb, tub, s, count, img_id
    except Exception as e:
        return None, None, 0, 0, 0


def not_timely(tub):
    # 如果滞后 1 分钟以上，说明有错误
    return tub < datetime.now() - timedelta(minutes=1)
