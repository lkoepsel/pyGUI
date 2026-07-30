#!/usr/bin/env -S uv run python
from guizero import App, Text, PushButton

import guisetup

guisetup.configure()  # macOS/uv: point tkinter at its Tcl/Tk data before creating a window


# Functions -----------------------------------------------------------
def pressed():
    print("Button was pressed")
    button.text(color="red", size=24, font="courier")
    button.text = "PRESSED!"


def move():
    # Screen dimensions, from the underlying tkinter window
    screen_w = app.tk.winfo_screenwidth()
    screen_h = app.tk.winfo_screenheight()

    # Bottom-right quadrant: half the screen in each direction,
    # positioned at the screen's midpoint
    w = screen_w // 2
    h = screen_h // 2
    x = screen_w // 2
    y = screen_h // 2

    app.tk.geometry(f"{w}x{h}+{x}+{y}")


app = App(
    title="Button App", visible=False
)  # start hidden: no flash at the default position
move()
Text(app, text="Welcome to the button app!")
button = PushButton(app, pressed, text="Press me!")
app.show()
app.display()
