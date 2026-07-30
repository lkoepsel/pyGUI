# Developing a Python GUI Lesson

This repository contains test code and instructional material for teaching
community college students how to program in Python. Specifically, **tkinter**
and a library called **guizero** are used to help students understand
object-oriented programming as well as GUI development — content that is more
interesting to students than text-based programs and procedural programming.

## Libraries

* [tkinter](https://docs.python.org/3/library/tkinter.html) — Python's built-in
  GUI library.
* [guizero](https://github.com/lawsie/guizero) — a wrapper for tkinter designed
  to make it easier for students to learn how to program GUI programs.

## Installation

The development platform for this course is **[Thonny](https://thonny.org)** —
a free Python editor built for beginners. It runs the same way on macOS,
Windows, and Linux, and on macOS/Windows it **bundles its own Python with
tkinter already working**, so there is nothing else to install or configure.

### 1. Install Thonny

Download the installer for your system from [thonny.org](https://thonny.org)
and run it.

* **macOS / Windows:** the installer includes Python and tkinter — you're done.
* **Linux:** install with your package manager (e.g.
  `sudo apt install thonny`), which brings in Python and Tk support. If
  tkinter is ever missing, `sudo apt install python3-tk` fixes it.

### 2. Verify tkinter

Open Thonny. In the **Shell** pane at the bottom, type:

```python
import tkinter
```

If nothing is printed (no error), tkinter is ready.

### 3. Install guizero

In Thonny: **Tools → Manage packages…**, search for `guizero`, click
**Install**. That's it — guizero is now available in every program you write.

### 4. Get this repository

Either clone it:

```bash
git clone git@github.com:lkoepsel/pyGUI.git
```

or use GitHub's **Code → Download ZIP** button and unzip it.

### 5. Run your first program

In Thonny: **File → Open…**, choose `hello/hello_tk.py`, and click the **Run**
button (or press **F5**). A small window appears. Then try
`hello/hello_guizero.py` — the same idea, written with guizero.

`hello_tk.py`:

```python
import tkinter as tk

app = tk.Tk()
app.title("Hello tkinter")
tk.Label(app, text="Hello, tkinter!").pack(padx=20, pady=20)
app.mainloop()
```

`hello_guizero.py`:

```python
from guizero import App, Text

app = App(title="Hello guizero")
Text(app, text="Hello, guizero!")
app.display()
```

## Lessons

* [`hello/`](hello) — minimal first programs in tkinter and guizero.
* [`lesson_1/`](lesson_1) — the Button App: callbacks, styling widget
  properties, and window placement. See its
  [README](lesson_1/README.md) for a section-by-section walkthrough.

## Experimenting in the Shell

Thonny's Shell is a full Python REPL using the same Python your programs run
with — a great way to explore. Create a window live and change it one line at
a time (don't call `app.display()` in the Shell; that's only for programs):

```python
>>> from guizero import App, Text
>>> app = App(title="live")      # a window appears
>>> t = Text(app, text="hello")  # text appears in it
>>> t.color = "red"              # ...and turns red as you type
```

## Notes

### Commenting shortcuts on macOS

Thonny's menu lists **Alt+3** (Comment out) and **Alt+4** (Uncomment), but on a
Mac those keys type the `£` and `¢` characters instead — the shortcuts never
reach Thonny. Use **⌘3** (**Edit → Toggle comment**) instead: select the lines
and press ⌘3 to comment them, ⌘3 again to uncomment. One shortcut does both.

If you prefer a different key (for example ⌘/, as used by many other editors),
Thonny reads shortcut overrides from its configuration file:

1. **Quit Thonny completely first.** This step matters: Thonny rewrites its
   configuration file when it exits, so any edit made while Thonny is running
   is silently erased.
2. Open `~/Library/Thonny/configuration.ini` in a text editor and add:

   ```ini
   [shortcuts]
   toggle_comment = <Command-Key-slash>
   ```

3. Start Thonny. **Edit → Toggle comment** now responds to ⌘/.
