from datetime import datetime


def interp(count: int):
    if count < 10:
        return '可以速通'
    else:
        return '不可速通'


def send(tlb: datetime, tub: datetime, res: int, cnt: int):
    tlbstr = datetime.strftime(tlb, "%H:%M:%S")
    tubstr = datetime.strftime(tub, "%H:%M:%S")
    return f'【核酸人少通知】\n目前核酸人多指数为{"%.1f" % res}，{interp(res)}！\n样本时间段：{tlbstr}至{tubstr}\n样本容量：{cnt}'


def send_img(img_id: int):
    # As images update frequently, we didn't check id validity.
    return f'[CQ:image,file={img_id}.jpg]'


if __name__ == '__main__':
    print(interp(4.4))
    print(interp(2.3))
    print(interp(5.7))
