# Developing a Python GUI Lesson

This folder contains test code and instructional material for teaching community college students how to program in Python. Specifically, tkinter and a repository called guizero will be used to help students understand object-oriented programming as well as GUI development. I believe providing content covering these two topics will be more interesting to students as compared to text-based programming along with procedural programming.

## Libraries

* tkinter - python's GUI library
* guizero - a wrapper for tkinter designed to make it easier for students to learn how to program GUI programs, it is located at [guizero](https://github.com/lawsie/guizero)

## Development platform

The development platform for students is **Thonny** (thonny.org). It bundles a
Python with working tkinter on macOS/Windows and provides its own package
manager (Tools → Manage packages) for installing guizero — no command-line
tooling required. Student-facing setup and run instructions live in
[README.md](README.md).

Lesson code should stay Thonny-friendly: plain `.py` files, no shebangs, no
environment-specific helpers — students open a file and press Run.

## Branches

* `main` — the Thonny-based course content (this branch).
* `vscode` — preserves the earlier VS Code + uv setup; see `VSCODE.md` on that
  branch for its requirements.
