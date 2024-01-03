[简体中文 (Chinese)](./README.ZH-CN.md)
# circuitpython-easybutton
- Multiple button state recognition implemented using loops. Executes specified functions when a button is pressed. Suitable for `circuitpython`.

### Features
- Executes a function at regular intervals after a button press.
- Executes a function when a button is released after a short press.
- Executes a function when a button is released after a long press.
- Executes a function when a button is pressed.
- Executes a function when a button is released.

### Notes
- `./main.py` is the sample file demonstrating usage.
- `./lib/easybutton.py` is the library file for the buttons.

### Example
- In this example, the button is connected to the pin with a ground connection.

```python
import board
import digitalio
from lib.easybutton import EasyButton, Button

# Configure the button pin
pin = digitalio.DigitalInOut(board.GP0)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.DOWN


# Define functions, they can be defined first or later used as anonymous functions
def test():
    print("^ UP ^")


b = Button(pin)
# Set trigger functions for the button
b.up_func = test  # Executed when the button is released
b.down_func = lambda: print("v DOWN v")  # Executed when the button is pressed
b.long_func = lambda: print("+ LONG +")  # Executed when the button is long pressed and released
b.hold_func = lambda: print("| HOLD |")  # Executed at regular intervals after the button is pressed
b.short_func = (print, "- SHORT -")  # Executed when the button is short pressed and released
eb = EasyButton(interval=100)
eb.add(b)
eb.run()
```