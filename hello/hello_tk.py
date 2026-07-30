#!/usr/bin/env -S uv run python
import guisetup  # noqa: F401  -- macOS/uv: let tkinter find its Tcl/Tk data; must be first
import tkinter as tk

app = tk.Tk()
app.title("Hello tkinter")
tk.Label(app, text="Hello, tkinter!").pack(padx=20, pady=20)
app.mainloop()
