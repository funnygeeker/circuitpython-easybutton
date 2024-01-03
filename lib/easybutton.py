# Github: https://github.com/funnygeeker/micropython-easybutton
# Author: funnygeeker (稽术宅)
# License: MIT

import time


def _call(func, *args):
    """
    调用函数并传递参数
        如果 func 是可调用对象，则执行 func(*args)
        如果 func 是元组且第一个元素为可调用对象，则执行 func[0](*(func[1] + args))

    Args:
        func: 函数或函数元组
        *args: 传递给函数的参数
    """
    if callable(func):
        func(*args)
    elif type(func) is tuple and callable(func[0]):
        in_args = func[1] if type(func[1]) is tuple or type(func[1]) is list else (func[1],)
        func[0](*tuple(list(in_args) + list(args)))


class Button:
    def __init__(self, pin, up: int = 1, down: int = 1, hold: int = 3, long: int = 5):
        """
        创建一个按钮实例

        Args:
            pin: 按钮引脚 (button pin)
            up: 判断为抬起所需的检测次数 (number of consecutive reads to determine button release)
            down: 判断为按下所需的检测次数 (number of consecutive reads to determine button press)
            hold: 按下后的每个周期的检测次数 (number of consecutive reads after button press for each cycle)
            long: 按钮按下行为判定为长按的检测次数 (number of consecutive reads to determine long button press)

        Notice:
            初始化完成后，请勿修改 down, hold, long 的值，或者在保持 self.status 列表长度大于等于以上变量的 (最大值 +1) 时修改
            (After initialization, please do not modify the values of `down`, `hold`, and `long`, or modify when
            `self.status` list length is greater than or equal to (max value + 1) of the above variables.)
        """
        self.pin = pin
        self.up = up
        self.down = down
        self.hold = hold
        self.hold_count = 0
        self.long = long
        self.status = [0] * (max(down, hold, long) + 1)
        self.up_func = None
        self.down_func = None
        self.long_func = None
        self.hold_func = None
        self.short_func = None


class EasyButton:
    def __init__(self, btn_list=None, interval: int = 20):
        """
        创建 EasyButton 实例

        Args:
            btn_list: 按钮列表 (button list)
            interval: 两次按键的检测间隔时间，单位：毫秒 (interval time between two button detections, in milliseconds)
        """
        if btn_list is None:
            btn_list = []
        self.button = btn_list
        self.interval = interval

    def add(self, button):
        """
        添加一个按钮 (add a button)
        """
        self.button.append(button)

    @staticmethod
    def _check(lst, n, v=1):
        if len(lst) < n:
            return False
        return all(value == v for value in lst[-n:])

    def detection(self):
        """
        检测一次按键 (Detect the key once)
        """
        for b in self.button:
            b_status = b.status
            if b.pin.value:
                b_status.pop(0)
                b_status.append(1)
            else:
                b_status.pop(0)
                b_status.append(0)
            # 检查按钮是否被按下，并且未被认为是长按
            if self._check(b_status, b.down) and not b_status[-b.down - 1]:
                # 执行按下按钮的回调函数
                _call(b.down_func)
            # 检查按钮是否被抬起
            elif not self._check(b_status[:-1], b.up, 0) and not b_status[-1]:
                # 如果按钮被按下的次数达到了 "长按" 的要求
                if self._check(b_status[:-1], b.long):
                    # 执行长按按钮的回调函数
                    _call(b.long_func)
                # 如果按钮被按下的次数未达到了 "长按" 的要求，判定为短按
                else:
                    # 执行短按按钮的回调函数
                    _call(b.short_func)
                # 执行按钮抬起的回调函数
                _call(b.up_func)
            # 检查按钮是否连续按住并达到了触发次数的要求
            elif self._check(b_status, b.hold):
                if b.hold_count == 0:
                    b.hold_count = b.hold
                else:
                    if b.hold_count <= 1:
                        # 执行连续按住按钮的回调函数
                        _call(b.hold_func)
                        b.hold_count = b.hold
                    else:
                        b.hold_count -= 1
            else:
                b.hold_count = 0

    def run(self):
        """
        持续检测按键 (Continuously detect keys)
        """
        while 1:
            self.detection()
            time.sleep(self.interval / 1000)
