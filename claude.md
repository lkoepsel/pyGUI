# Developing a Python GUI Lesson

This folder contains test code and instructional material for teaching community college students how to program in Python. Specifically, tkinter and a repository called guizero will be used to help students understand object-oriented programming as well as GUI development. I believe providing content covering these two topics will be more interesting to students as compared to text-based programming along with procedural programming.

## Libraries

* tkinter - python's GUI library
* guizero - a wrapper for tkinter dsigned to make it easier for students to learn how to program GUI programs, it is located at [guizero](https://github.com/lawsie/guizero)

## Installation

The tool to use this repository is `uv`. the steps required are the following:

> **macOS note:** tkinter needs the Tk graphics library. The Python that ships
> with macOS (and Homebrew's `python@3.x`) often does **not** include a working
> tkinter. To avoid this, we tell `uv` to use its own *managed* Python builds,
> which come with tkinter already included. Steps 3–4 below handle this.

### 1. Install `uv`

If you do not already have `uv`, install it (macOS/Linux):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart your terminal and confirm it works:

```bash
uv --version
```

### 2. Create the project

From inside this folder, initialize a `uv` project. This creates a
`pyproject.toml` and a virtual environment for your dependencies.

```bash
uv init
```

### 3. Use a tkinter-ready Python

Install and pin a `uv`-managed Python (these builds include tkinter):

```bash
uv python install 3.12
uv python pin 3.12
```

To make sure `uv` never falls back to a system Python that is missing tkinter,
add this to `pyproject.toml`:

```toml
[tool.uv]
python-preference = "only-managed"
```

### 4. Verify tkinter works

`tkinter` is part of Python's standard library, so there is nothing to install.
First confirm it imports:

```bash
uv run python -c "import tkinter; print('tkinter OK, Tk', tkinter.TkVersion)"
```

You should see something like `tkinter OK, Tk 9.0`.

> **macOS gotcha (managed Python):** importing `tkinter` succeeds, but actually
> *opening a window* can fail inside the project's `.venv` with
> `TclError: Cannot find a usable init.tcl`. uv's managed Python ships the Tcl/Tk
> data files, but Tcl looks for them relative to the venv, where they were never
> copied. This repo includes a small helper, **`guisetup.py`**, that fixes this:
> import it *before* `tkinter`/`guizero` and it points Tcl/Tk at the right files.
> It is a no-op on Windows/Linux or with a Homebrew Python.

To confirm a window really opens:

```bash
uv run python -c "import guisetup, tkinter as tk; r=tk.Tk(); r.after(500, r.destroy); r.mainloop(); print('window OK')"
```

A small window flashes on screen and you get `window OK`.

### 5. Add guizero

`guizero` is a third-party package, so add it as a project dependency:

```bash
uv add guizero
```

`uv` records it in `pyproject.toml` and installs it into the project's
environment.

### 6. Run your first programs

Two ready-to-run examples ship with this repo. Two lines at the top of each make
them easy to run:

* `#!/usr/bin/env -S uv run python` — a *shebang* that lets you run the file
  directly; the OS hands it to `uv`, which uses the project's Python and
  dependencies. Must be the very first line.
* `import guisetup` — the macOS/uv fix described in step 4. Keep it above the
  `tkinter`/`guizero` imports. (On Windows or Linux it does nothing, so the same
  file runs everywhere.)

`hello_tk.py`:

```python
#!/usr/bin/env -S uv run python
import guisetup  # noqa: F401  -- macOS/uv: let tkinter find its Tcl/Tk data; must be first
import tkinter as tk

app = tk.Tk()
app.title("Hello tkinter")
tk.Label(app, text="Hello, tkinter!").pack(padx=20, pady=20)
app.mainloop()
```

`hello_guizero.py`:

```python
#!/usr/bin/env -S uv run python
import guisetup  # noqa: F401  -- macOS/uv: let tkinter find its Tcl/Tk data; must be first
from guizero import App, Text

app = App(title="Hello guizero")
Text(app, text="Hello, guizero!")
app.display()
```

Mark each program as executable **once** (the two shipped examples already are):

```bash
chmod +x hello_tk.py hello_guizero.py main.py
```

Then run it directly from the project folder:

```bash
./hello_tk.py
./hello_guizero.py
```

The `./` tells the shell to run the file in the current folder. `uv run` still
works too, and does not need `chmod`:

```bash
uv run python hello_tk.py
```

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
