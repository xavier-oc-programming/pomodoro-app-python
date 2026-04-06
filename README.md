# pomodoro-app-python

A tkinter Pomodoro timer that cycles through work and break sessions automatically, tracking completed sessions with checkmarks.

---

## Table of Contents

1. [Quick start](#1-quick-start)
2. [Builds comparison](#2-builds-comparison)
3. [Controls](#3-controls)
4. [App flow](#4-app-flow)
5. [Features](#5-features)
6. [Navigation flow](#6-navigation-flow)
7. [Architecture](#7-architecture)
8. [Module reference](#8-module-reference)
9. [Configuration reference](#9-configuration-reference)
10. [Display layout](#10-display-layout)
11. [Design decisions](#11-design-decisions)
12. [Course context](#12-course-context)
13. [Dependencies](#13-dependencies)

---

## 1. Quick start

```bash
# From repo root — interactive menu
python menu.py          # select 1 (original) or 2 (advanced)

# Or run builds directly
python original/main.py
python advanced/main.py
```

---

## 2. Builds comparison

| Feature | Original | Advanced |
|---|---|---|
| Pomodoro session sequencing | ✔ | ✔ |
| Countdown via `root.after()` | ✔ | ✔ |
| Tomato canvas image | ✔ | ✔ |
| Start / Reset buttons | ✔ | ✔ |
| Checkmark session tracker | ✔ | ✔ |
| Session-type colour coding | ✔ | ✔ |
| OOP split (logic / display) | ✗ | ✔ |
| `config.py` — zero magic numbers | ✗ | ✔ |
| Pure-logic `PomodoroTimer` class | ✗ | ✔ |
| Injected callbacks (decoupled UI) | ✗ | ✔ |
| `sys.path.insert` for menu launch | ✗ | ✔ |

---

## 3. Controls

### Both builds

| Control | Action |
|---|---|
| **Start** button | Begin / advance to the next session |
| **Reset** button | Cancel countdown, reset counter and display |

> There is no keyboard binding — this app is mouse-only.

---

## 4. App flow

1. Run `menu.py` (or a build directly).
2. The window opens showing "Timer" label, tomato canvas, and `00:00`.
3. Click **Start** → the first work session begins (25:00 countdown, "Work" in green).
4. Countdown ticks every second via `root.after()`.
5. When the countdown reaches `00:00` it automatically triggers the next session:
   - Sessions 1, 3, 5, 7 → work (25 min, green).
   - Sessions 2, 4, 6 → short break (5 min, pink).
   - Session 8 → long break (20 min, red).
6. A ✔ is added to the checkmark row after each completed work session.
7. Clicking **Reset** at any time cancels the countdown and returns to the initial state.

---

## 5. Features

### Both builds

**Automatic session sequencing** — when a countdown reaches zero the next session starts immediately without user interaction, following the classic Pomodoro schedule (work → short break → work → … → long break).

**Session-type colour coding** — the title label changes colour to communicate the current session type: green for work, pink for short breaks, red for long breaks.

**Checkmark progress tracker** — a ✔ symbol is appended below the timer after each completed work session, giving a visual tally of focus blocks done in the current cycle.

**Non-blocking countdown** — the timer uses `root.after()` rather than `time.sleep()`, so the UI remains responsive throughout.

### Advanced build only

**`PomodoroTimer` pure-logic class** — session sequencing and checkmark computation live in a class with no tkinter dependency, making the logic independently testable.

**`Display` class with injected callbacks** — the UI owns all widgets and the countdown loop but contains zero application logic. Every user action is delegated to a callback supplied by `main.py`.

**`config.py` single source of truth** — every colour, font size, duration, and window dimension is defined once and referenced everywhere. No magic numbers appear in any other file.

---

## 6. Navigation flow

### a) Terminal menu tree

```
python menu.py
│
├── 1  →  subprocess.run(original/main.py)
│         (returns to menu when window closes)
│
├── 2  →  subprocess.run(advanced/main.py)
│         (returns to menu when window closes)
│
└── q  →  exit
```

### b) In-app flow

```
┌─────────────────────┐
│   IDLE  ("Timer")   │  ← initial state / after Reset
│     display 00:00   │
└─────────────────────┘
         │
    [Start clicked]
         │
         ▼
┌─────────────────────┐
│  WORK SESSION       │  reps = 1, 3, 5, 7
│  title: "Work" 🟢   │  countdown: 25:00
│  root.after ticking │
└─────────────────────┘
         │                          │
  countdown hits 00:00         [Reset clicked]
         │                          │
         ▼                          ▼
┌─────────────────────┐   ┌─────────────────────┐
│  SHORT BREAK        │   │   IDLE              │
│  title: "Break" 🩷  │   │   display 00:00     │
│  countdown: 5:00    │   │   checkmarks cleared│
└─────────────────────┘   └─────────────────────┘
         │
  countdown hits 00:00 (rep 8 → long break)
         │
         ▼
┌─────────────────────┐
│  LONG BREAK         │
│  title: "Break" 🔴  │
│  countdown: 20:00   │
└─────────────────────┘
         │
  countdown hits 00:00
         │
         └── loop back to WORK SESSION (reps resets via full cycle)
```

---

## 7. Architecture

```
pomodoro-app-python/
│
├── menu.py                  # Terminal menu — launches builds via subprocess
├── art.py                   # LOGO ASCII art string
├── requirements.txt         # Stdlib only; Python 3.10+ note
├── .gitignore
├── README.md
│
├── docs/
│   └── COURSE_NOTES.md      # Original exercise description and concepts
│
├── original/
│   ├── main.py              # Course exercise (path fix only)
│   └── tomato.png           # Tomato image asset
│
└── advanced/
    ├── config.py            # All constants — zero magic numbers elsewhere
    ├── timer.py             # PomodoroTimer — pure session logic, no tkinter
    ├── display.py           # Display — owns Tk root, widgets, countdown loop
    ├── main.py              # Orchestrator — instantiates and wires everything
    └── tomato.png           # Tomato image asset
```

---

## 8. Module reference

### `advanced/timer.py` — `PomodoroTimer`

| Method | Returns | Description |
|---|---|---|
| `advance()` | `tuple[int, str, str]` | Increment reps; return `(duration_sec, title_text, title_colour)` |
| `reset()` | `None` | Reset session counter to zero |
| `checkmarks` *(property)* | `str` | One ✔ per completed work session |

### `advanced/display.py` — `Display`

| Method | Returns | Description |
|---|---|---|
| `__init__(tomato_path, on_start, on_reset, on_tick_complete)` | — | Build window and all widgets |
| `start_countdown(seconds)` | `None` | Begin countdown from `seconds` |
| `stop_countdown()` | `None` | Cancel running countdown without firing `on_tick_complete` |
| `render_timer(text)` | `None` | Update the canvas countdown text |
| `render_title(text, color)` | `None` | Update the session-type label |
| `render_checkmarks(text)` | `None` | Update the checkmark row label |
| `close()` | `None` | Exit via `sys.exit(0)` |

---

## 9. Configuration reference

All constants live in [advanced/config.py](advanced/config.py).

| Constant | Default | Description |
|---|---|---|
| `WINDOW_TITLE` | `"Pomodoro"` | Tk window title |
| `WINDOW_PAD_X` | `100` | Horizontal padding (px) |
| `WINDOW_PAD_Y` | `50` | Vertical padding (px) |
| `CANVAS_WIDTH` | `200` | Canvas width (px) |
| `CANVAS_HEIGHT` | `224` | Canvas height (px) |
| `PINK` | `"#e2979c"` | Short-break title colour |
| `RED` | `"#e7305b"` | Long-break title colour |
| `GREEN` | `"#9bdeac"` | Work-session title colour / checkmarks |
| `YELLOW` | `"#f7f5dd"` | Window background colour |
| `FONT_NAME` | `"Courier"` | Font family for all labels |
| `FONT_TITLE_SIZE` | `50` | Session-type label font size |
| `FONT_TIMER_SIZE` | `35` | Countdown text font size |
| `FONT_CHECKS_SIZE` | `25` | Checkmarks label font size |
| `TICK_MS` | `1000` | Milliseconds per countdown tick |
| `WORK_MIN` | `25` | Work session duration (minutes) |
| `SHORT_BREAK_MIN` | `5` | Short break duration (minutes) |
| `LONG_BREAK_MIN` | `20` | Long break duration (minutes) |
| `LONG_BREAK_EVERY` | `8` | Rep number that triggers a long break |
| `SHORT_BREAK_MODULO` | `2` | Even reps trigger short breaks |

---

## 10. Display layout

```
  ┌──────────────────────────────────────────────────────┐
  │  padx=100                              padx=100      │
  │  pady=50                                             │
  │                                                      │
  │         col 0     col 1         col 2               │
  │  row 0           "Timer"                             │
  │              (50pt Courier, green)                   │
  │                                                      │
  │  row 1        ┌──────────┐                           │
  │               │  200×224 │  ← Canvas                 │
  │               │  tomato  │    image centre: (100,112)│
  │               │  00:00   │    timer text:  (100,130) │
  │               └──────────┘                           │
  │                                                      │
  │  row 2  [Start]           [Reset]                    │
  │                                                      │
  │  row 3         ✔✔✔✔                                  │
  │              (25pt Courier, green)                   │
  │                                                      │
  └──────────────────────────────────────────────────────┘
```

---

## 11. Design decisions

**`display.py` owns all UI** — keeping every widget in one class means the logic in `timer.py` and `main.py` can be tested or swapped without touching the GUI layer. The display is a thin skin over the logic.

**`config.py` — zero magic numbers** — a single source of truth for colours, sizes, and durations. Changing `WORK_MIN` in one place updates both the logic and any future UI that displays it.

**Callbacks injected via `__init__`** — `Display` knows nothing about `PomodoroTimer`. The three callables (`on_start`, `on_reset`, `on_tick_complete`) are supplied by `main.py`, keeping `Display` fully decoupled and independently reusable.

**`root.after()` vs `mainloop()` inside `__init__`** — `Display.__init__` builds the window and starts no loop. `root.mainloop()` is called once at the end of `main()`. This keeps the call-stack clean and means `Display` can be constructed without blocking.

**`sys.path.insert` pattern** — `advanced/main.py` inserts its own directory at the front of `sys.path` so that sibling imports (`from config import ...`) work both when launched directly (`python advanced/main.py`) and when launched via `subprocess.run()` from `menu.py`.

**`subprocess.run` + `cwd=`** — `menu.py` passes `cwd=path.parent` so that each build runs with its own directory as the working directory. This ensures `Path(__file__).parent` resolves correctly for asset loading inside each build.

**`while True` in `menu.py` vs recursion** — a simple loop re-prints the menu after each build exits. Recursion would grow the call stack unboundedly if the user ran many sessions.

**Console cleared before every menu render** — `os.system("cls"/"clear")` runs at the top of each loop iteration so the menu is always presented on a clean terminal, regardless of output from the previous build.

**`sys.exit(0)` vs `root.destroy()`** — calling `root.destroy()` alone can raise tkinter cleanup errors on some platforms. `sys.exit(0)` terminates cleanly and is the standard pattern for GUI applications that close via a button.

---

## 12. Course context

Built as **Day 28** of *100 Days of Code* by Dr. Angela Yu.

**Concepts covered in the original build:**
- `tkinter` window, canvas, label, and button widgets
- `.grid()` layout with column/row
- `PhotoImage` and `canvas.create_image()`
- `canvas.create_text()` and `canvas.itemconfig()`
- `window.after()` for non-blocking timed callbacks
- `window.after_cancel()` to stop a scheduled callback
- `global` keyword for mutable module-level state
- `math.floor()` and f-string formatting with conditional zero-padding

**The advanced build extends into:**
- Object-oriented design: separating logic (`PomodoroTimer`) from UI (`Display`)
- Dependency injection via constructor callbacks
- Single-source-of-truth configuration (`config.py`)
- `sys.path` manipulation for portable imports
- Type hints including `tuple[...]`, `str | None`, `Callable[[], None]`

See [docs/COURSE_NOTES.md](docs/COURSE_NOTES.md) for the full concept breakdown.

---

## 13. Dependencies

| Module | Used in | Purpose |
|---|---|---|
| `tkinter` | `original/main.py`, `advanced/display.py` | GUI framework |
| `math` | `original/main.py`, `advanced/timer.py` | `floor()` for checkmark count |
| `sys` | `menu.py`, `advanced/main.py`, `advanced/display.py` | `sys.executable`, `sys.path`, `sys.exit()` |
| `os` | `menu.py` | `os.system()` for console clear |
| `subprocess` | `menu.py` | Launch builds as subprocesses |
| `pathlib` | `original/main.py`, `advanced/main.py`, `advanced/display.py` | Portable asset paths |
| `collections.abc` | `advanced/display.py` | `Callable` type hint |
