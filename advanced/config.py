# ── Screen ─────────────────────────────────────────────────────────────────────
WINDOW_TITLE = "Pomodoro"
WINDOW_PAD_X = 100
WINDOW_PAD_Y = 50
CANVAS_WIDTH = 200
CANVAS_HEIGHT = 224

# ── Colours ────────────────────────────────────────────────────────────────────
PINK = "#e2979c"    # short-break title colour
RED = "#e7305b"     # long-break title colour
GREEN = "#9bdeac"   # work-session title colour / checkmarks
YELLOW = "#f7f5dd"  # window background

# ── Fonts ──────────────────────────────────────────────────────────────────────
FONT_NAME = "Courier"
FONT_TITLE_SIZE = 50
FONT_TIMER_SIZE = 35
FONT_CHECKS_SIZE = 25

# ── Timing / delays ────────────────────────────────────────────────────────────
TICK_MS = 1000          # milliseconds between countdown ticks

# ── Session durations (minutes) ────────────────────────────────────────────────
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ── Session sequence rules ─────────────────────────────────────────────────────
LONG_BREAK_EVERY = 8    # every 8th rep triggers a long break
SHORT_BREAK_MODULO = 2  # even-numbered reps are short breaks
