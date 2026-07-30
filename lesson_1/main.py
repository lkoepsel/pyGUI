from guizero import App, Text, PushButton


# Functions -----------------------------------------------------------


# when the button is pressed, this function runs
# in this case, the text on the button changes
def pressed():
    button.text = "PRESSED!"
    button.text_color = "red"
    button.text_size = 24
    button.font = "Courier"


# guizero doesn't set the location of a window,
# however we can use tkinter, this command will move
# the window to the bottom, right quadrant of the screen
# menu_bar adjusts for the size of the menu_bar
def move():
    menu_bar = 50
    # Screen dimensions, from the underlying tkinter window
    screen_w = app.tk.winfo_screenwidth()
    screen_h = app.tk.winfo_screenheight()

    # Bottom-right quadrant: half the screen in each direction,
    # positioned at the screen's midpoint
    w = screen_w // 2
    h = screen_h // 2 - menu_bar
    x = screen_w // 2
    y = screen_h // 2 + menu_bar

    app.tk.geometry(f"{w}x{h}+{x}+{y}")


# start app as hidden, so no flash at the default position
app = App(title="Button App", visible=False)


# be sure to move it where you want it
move()

# setup the text for the app and create a button
Text(app, text="Welcome to my button app!")
button = PushButton(app, pressed, text="Press me!")

# show overwrites "visible=False" above, display puts it on the screen
app.show()
app.display()
