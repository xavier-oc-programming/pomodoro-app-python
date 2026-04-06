# Day 28 — Course Notes: Pomodoro Timer

## Exercise description

Build a GUI Pomodoro timer using tkinter.  
The app cycles automatically through work sessions and break sessions,
displaying the remaining time on a canvas and tracking completed sessions
with checkmark symbols.

### Requirements from the course

- Use tkinter to build the GUI.
- Display a tomato image on a `Canvas` widget using `PhotoImage`.
- Implement a recursive countdown using `window.after()` (not `time.sleep()`).
- Track how many reps have elapsed and derive session type from that count:
  - odd rep → work session (25 min, green title)
  - even rep (non-8) → short break (5 min, pink title)
  - every 8th rep → long break (20 min, red title)
- Automatically advance to the next session when the countdown reaches zero.
- Add one ✔ per completed work session below the timer.
- Reset button cancels the countdown and returns everything to the initial state.

### Concepts covered

- `tkinter` basics: `Tk`, `Canvas`, `Label`, `Button`, `.grid()` layout
- `PhotoImage` for displaying PNG assets
- `canvas.create_image()` and `canvas.create_text()`
- `canvas.itemconfig()` to update canvas text at runtime
- `window.after(ms, callback, *args)` for non-blocking timed callbacks
- `window.after_cancel(id)` to stop a scheduled callback
- `global` keyword for mutable module-level state
- `math.floor()` for integer division
- f-strings with conditional zero-padding
- Widget colour configuration with hex strings
