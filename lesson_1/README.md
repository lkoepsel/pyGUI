# Lesson 1: The Button App

This lesson builds a small GUI program with **guizero**: a window with a welcome message and a button that changes its own text and style when pressed. Along the way it introduces the most important idea in GUI programming — *event-driven code* — plus a few practical details about windows on macOS.

## Running the program

In Thonny: **File → Open…**, choose `lesson_1/main.py`, and do one of the following:
* click the **Run** button 
* press **F5**
* Cmd/Ctrl-r

A window appears in the bottom-right quadrant of your screen. Press the button and watch the text change.

---

## The code, section by section

### 1. Imports

```python
from guizero import App, Text, PushButton
```

We import the three guizero *classes* this program uses:

* `App` — the main window; every guizero program has exactly one
* `Text` — a label that displays a string at top of the window
* `PushButton` — a clickable button

### 2. The `pressed()` function — an event handler

```python
# when the button is pressed, this function runs
# in this case, the text on the button changes
def pressed():
    button.text = "PRESSED!"
    button.text_color = "red"
    button.text_size = 24
    button.font = "Courier"
```

This is the heart of event-driven programming. Notice that **nothing in the program calls `pressed()` directly**. Instead, the function name is passed to the button when the button is created (section 5), and *guizero* calls it every time the user clicks. A function used this way is called a **callback** (or *event handler*).

Inside the callback, the button restyles itself by **assigning to properties**:

| Property | What it changes |
|---|---|
| `text` | the label on the button |
| `text_color` | the color of the label |
| `text_size` | the size in points |
| `font` | the font family |

This is *guizero*'s programming style throughout: you *assign* to a property (`button.text_color = "red"`), you don't call a method. The window updates immediately on each assignment.

### 3. The `move()` function — dropping down to tkinter

```python
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
```

*guizero* is a *wrapper* around Python's *tkinter* library, it makes the common things easy, but it doesn't cover everything. Window position is one of the gaps. When *guizero* can't do something, we can use *tkinter* functionality underneath via **`app.tk`** and use *tkinter* directly, without giving up the simplicity of *guizero*.

Step by step:

* `winfo_screenwidth()` / `winfo_screenheight()` - ask tkinter how big the screen is, in pixels.
* We want the **bottom-right quadrant**: a window half the screen's width and height (`// 2` is *integer division* — pixel counts must be whole numbers), with its **top-left corner** at the screen's midpoint.
* `menu_bar = 50` nudges the numbers because the macOS menu bar takes up the top of the screen: the height is trimmed by 50 pixels and the window is pushed down 50 pixels, so it doesn't collide with the Dock or menu bar. (*For Windows, set it to 0.*)
* `geometry()` takes a specially formatted string:
  `"WIDTHxHEIGHT+X+Y"` — for example `"720x400+720+500"` means "make the window 720×400 pixels, and place its top-left corner 720 pixels from the left edge of the screen and 500 pixels down from the top." The `f"..."` is an **f-string**: Python fills in the variable values between the `{ }` braces.

### 4. Creating the app — hidden

```python
# start app as hidden, so no flash at the default position
app = App(title="Button App", visible=False)


# be sure to move it where you want it
move()
```

Creating an `App` normally puts a window on screen *immediately* — at a default position. If we moved it afterward, users would see it flash at the wrong spot and jump. The fix: create it with ` visible=False`, so the window exists (and can be measured and positioned) but is not shown yet. Then `move()` positions it while it is still invisible.

Order matters here: `move()` uses `app`, so it can only be called after `app` exists.

### 5. Adding the widgets

```python
# setup the text for the app and create a button
Text(app, text="Welcome to my button app!")
button = PushButton(app, pressed, text="Press me!")
```

Widgets are created by passing the *container* they belong to as the first argument — here, `app` — so guizero knows where to put them.

Two details worth noticing:

* The `Text` is never assigned to a variable, because we never need to talk to it again. The `PushButton` **is** assigned (`button = ...`) because `pressed()` needs to reach it to change its text.
* Look at the second argument: `pressed` — **no parentheses**. We are handing the button the function itself, so it can call it later, on every click. Writing `pressed()` (with parentheses) would call the
  function *once, right now*, and hand the button its return value — a classic beginner bug worth trying on purpose to see what happens.

### 6. Show the window and start the event loop

```python
# show overwrites "visible=False" above, display puts it on the screen
app.show()
app.display()
```

`app.show()` undoes the `visible=False` from section 4 — the window appears for the first time, already styled, populated, and in the right place.

`app.display()` starts guizero's **event loop**: an endless loop that waits for events (clicks, key presses, window moves) and runs the matching callbacks — like our `pressed()`. The program stays "stuck" on this line until the window is closed; that's normal, and it's why `display()` is always the *last* line. **Any code written after it won't run until the app quits.**

---

## Things to try

1. Change the button's `text_color` to another color, or try a hex value like `"#3366ff"`.
2. Move the window to the **top-left** quadrant instead. (Which of `x`, `y`, `w`, `h` change?)
3. Change `PushButton(app, pressed, ...)` to `PushButton(app, pressed(), ...)` and observe what happens, and when `pressed()` actually runs. Then change it back!
