from datetime import datetime
import requests

# Configuration

img_buffer = 20
interval = 10

# Temp

img_id = 0


def append(res: int):
    # Get data
    t = datetime.now()

    # Form data
    data = {
        'count': res,
        'img_id': img_id
    }

    # Post data
    try:
        requests.post('http://nab-server:8000/entry/', data=data)
    except Exception as e:
        print(f'[Error] Post data failed: {e}')


def get_next_img_id():
    global img_id, img_buffer
    img_id += 1
    if img_id >= img_buffer:
        img_id = 0
    return img_id
