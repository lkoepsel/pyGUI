#!/usr/bin/env -S uv run python
import guisetup
from guizero import App, Text

app = App(title="Hello guizero")
Text(app, text="Hello, guizero!")
app.display()
