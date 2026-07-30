#!/usr/bin/env -S uv run python
import tkinter as tk

import guisetup

guisetup.configure()  # macOS/uv: point tkinter at its Tcl/Tk data before creating a window

app = tk.Tk()
app.title("Hello tkinter")
tk.Label(app, text="Hello, tkinter!").pack(padx=20, pady=20)
app.mainloop()
