"""Make tkinter find its Tcl/Tk data files under uv's managed Python on macOS.

uv's managed CPython ships the Tcl/Tk graphics library, but when you run inside
a project virtual environment Tcl searches for its data files (``init.tcl``)
relative to the venv, where they were never copied.  Creating a window then
fails with::

    _tkinter.TclError: Cannot find a usable init.tcl in the following directories

This module points ``TCL_LIBRARY`` / ``TK_LIBRARY`` at the real files inside the
base interpreter, computed at runtime so it keeps working across Python patch
updates.  Importing ``tkinter``/``guizero`` is fine without it; only *creating a
window* needs the variables, so call ``configure()`` any time before the first
``Tk()`` / ``App()``::

    import guisetup
    import tkinter as tk

    guisetup.configure()  # before creating a window
    root = tk.Tk()

It is a no-op if the variables are already set or the data can't be found, so it
is harmless on Windows/Linux or with a Homebrew Python.
"""

import glob
import os
import sys


def _find_data_dir(marker):
    """Return the first ``lib/<name>`` dir under the base prefix holding *marker*."""
    for path in sorted(glob.glob(os.path.join(sys.base_prefix, "lib", "t*"))):
        if os.path.isfile(os.path.join(path, marker)):
            return path
    return None


def configure():
    if not os.environ.get("TCL_LIBRARY"):
        tcl = _find_data_dir("init.tcl")  # e.g. .../lib/tcl9.0
        if tcl:
            os.environ["TCL_LIBRARY"] = tcl
    if not os.environ.get("TK_LIBRARY"):
        tk = _find_data_dir("tk.tcl")  # e.g. .../lib/tk9.0
        if tk:
            os.environ["TK_LIBRARY"] = tk
