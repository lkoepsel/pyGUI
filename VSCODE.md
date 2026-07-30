# Using VS Code with this repository

This branch (`vscode`) preserves the VS Code + `uv` development setup for the
pyGUI lessons. The `main` branch uses Thonny instead; everything specific to
VS Code and `uv` lives here. This file documents what is required to be
successful with this setup.

## Overview of the toolchain

* **uv** manages Python itself, the virtual environment, and dependencies.
* **VS Code** with the Python + Pylance extensions is the editor; **Ruff**
  handles linting.
* A small local module, **`guisetup.py`**, works around a macOS-specific
  tkinter issue (explained below).

## 1. Install uv

macOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart the terminal, then confirm: `uv --version`.

## 2. Set up the project

After cloning, from the project folder:

```bash
uv sync
```

This single command:

* installs the pinned Python (see `.python-version`) as a **uv-managed** build,
* creates `.venv/`,
* installs `guizero`,
* installs the project itself, which makes the local `guisetup` module
  importable from any lesson folder.

### Why uv-managed Python matters (macOS)

The Pythons already on a Mac (Apple's, Homebrew's) often **lack a working
tkinter**. uv's managed builds include Tk. Two settings enforce this:

* `.python-version` pins the version.
* `pyproject.toml` contains:

  ```toml
  [tool.uv]
  python-preference = "only-managed"
  ```

  so uv never silently falls back to a tkinter-less system Python.

### The `guisetup` module and the init.tcl problem

With uv's managed Python, `import tkinter` succeeds but **creating a window
fails inside the venv**:

```
_tkinter.TclError: Cannot find a usable init.tcl in the following directories: ...
```

Tcl searches for its data files relative to the venv, where they were never
copied. `guisetup.py` (project root) fixes this at runtime by deriving
`TCL_LIBRARY`/`TK_LIBRARY` from the base interpreter. It is installed into the
environment via the `[build-system]`/hatchling config in `pyproject.toml`, so
any lesson file can use it.

**Pattern for every GUI program** — imports at the top as usual, and call
`configure()` any time *before the first window is created* (imports are safe;
only `Tk()`/`App()` needs it):

```python
from guizero import App, Text

import guisetup

guisetup.configure()  # macOS/uv: point tkinter at its Tcl/Tk data before creating a window

app = App(title="...")
```

On Windows/Linux (or a Homebrew Python with Tk), `configure()` is a no-op, so
the same file runs everywhere.

## 3. VS Code configuration

`.vscode/settings.json` points VS Code at the project environment:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.analysis.extraPaths": ["${workspaceFolder}"]
}
```

Without this, Pylance reports `Import "guizero" could not be resolved`. If that
warning appears anyway:

* Command Palette → **Python: Select Interpreter** → `./.venv/bin/python`, or
* **Developer: Reload Window** after `uv sync` creates `.venv`.

### Ruff and import order

Keep imports in canonical groups — standard library / third-party first, then
the local `guisetup` in its own group, then the `configure()` call **after**
the import block (as in the pattern above). This satisfies both `E402`
("import not at top of file") and `I001` (isort) with **no `# noqa` comments
and no ruff configuration**. Do not put `guisetup.configure()` between imports;
that trips E402 in editors that enable it.

## 4. Running programs

Each program starts with a shebang line that routes execution through uv:

```python
#!/usr/bin/env -S uv run python
```

Mark a program executable **once**:

```bash
chmod +x lesson_1/main.py
```

Then run it directly:

```bash
./lesson_1/main.py
```

`uv run python lesson_1/main.py` always works too (no chmod needed). Both use
the project's Python and installed packages, from the project root or from
inside a lesson folder (uv walks up to find the project).

## 5. REPL workflow (live experimentation)

In VS Code's integrated terminal:

```bash
uv run python
```

guarantees the project environment. Or Command Palette → **Python: Start
Terminal REPL** (uses the selected interpreter). **Shift+Enter** sends the
current line/selection from the editor to a REPL.

GUI-specific: **don't call `app.display()` in the REPL** — it blocks the
prompt. In an interactive session tkinter keeps windows responsive while you
type, so you can build and restyle a GUI live:

```python
>>> import guisetup
>>> guisetup.configure()
>>> from guizero import App, Text
>>> app = App(title="live")     # window appears immediately
>>> t = Text(app, text="hello")
>>> t.color = "red"             # updates on screen as you type
```

If a session gets into a bad state, exit (`Ctrl+D`) and restart the REPL.

## Security

You may wonder why you have to type `./hello_tk.py` instead of just
`hello_tk.py`. When you type a bare command, the shell searches a list of
folders called `PATH` (things like `/usr/bin`) to find the program — and, by
design, it does **not** look in the folder you are currently in. Writing `./`
says "run *this* file, right here," which is why it is required.

It is tempting to "fix" this by adding the current folder (`.`) to `PATH` so
bare names work everywhere. **Don't** — it is a classic security mistake:

* **Trojaned commands.** Suppose an attacker drops a file named `ls` (or `git`,
  or `python`) into a shared or downloaded folder. With `.` on your `PATH`, the
  moment you `cd` into that folder and type `ls`, you run *their* program
  instead of the real one — with your permissions. Without `.` on `PATH`, the
  real `/bin/ls` is found first and the malicious file is ignored unless you
  deliberately run `./ls`.
* **Typo hijacking.** A malicious file named `sl`, `gti`, or `grpe` can lie in
  wait for a common mistype and run automatically.
* **It depends on where you stand.** With `.` on `PATH`, what a command does
  changes based on which folder you happen to be in — the same word can run
  different programs. That is confusing and unpredictable.

The safe habit is the one this project uses: keep `.` **off** your `PATH`, and
run local programs explicitly with `./name`. The extra two characters are a
deliberate, visible choice to run code from the current folder.
