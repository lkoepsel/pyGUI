#!/usr/bin/env -S uv run python
import guisetup  # noqa: F401  -- macOS/uv: let tkinter find its Tcl/Tk data; must be first
from guizero import App, Text

app = App(title="Hello guizero")
Text(app, text="Hello, guizero!")
app.display()
