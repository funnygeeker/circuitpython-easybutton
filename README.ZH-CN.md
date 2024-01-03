[English (英语)](./README.md)
# circuitpython-easybutton
- 使用循环实现的多种按钮状态识别，按钮按下时执行指定函数，适用于 `circuitpython`

### 功能
- 按钮按下后，每隔一段时间执行一次函数
- 按钮短按后，松开时执行函数
- 按钮长按后，松开时执行函数
- 按钮按下时执行函数
- 按钮松开时执行函数

### 说明
`./main.py` 为使用示例文件
`./lib/easybutton.py` 为按钮库文件

### 示例
- 在本次示例中，按钮所在的引脚接按钮，按钮接的是 `GND`

```python
import board
import digitalio
from lib.easybutton import EasyButton, Button

# 配置按钮引脚
pin = digitalio.DigitalInOut(board.GP0)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.DOWN


# Define functions, they can be defined first or later used as anonymous functions
# 定义函数，可以先定义，也可以后续使用匿名函数
def test():
    print("^ UP ^")


b = Button(pin)
# Set trigger functions for the button
b.up_func = test  # Executed when the button is released  # 按钮松开时执行函数
b.down_func = lambda: print("v DOWN v")  # Executed when the button is pressed  # 按钮按下时执行
b.long_func = lambda: print("+ LONG +")  # Executed when the button is long pressed and released  # 按钮长按后，松开时执行
b.hold_func = lambda: print("| HOLD |")  # Executed at regular intervals after the button is pressed  # 按钮按下后，每隔一段时间执行一次
b.short_func = (print, "- SHORT -")  # Executed when the button is short pressed and released  # 按钮短按后，松开时执行
eb = EasyButton(interval=100)
eb.add(b)
eb.run()
```
