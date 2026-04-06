import sys
from pathlib import Path
from tkinter import Tk, Canvas, Label, Button, PhotoImage
from collections.abc import Callable

from config import (
    WINDOW_TITLE, WINDOW_PAD_X, WINDOW_PAD_Y,
    CANVAS_WIDTH, CANVAS_HEIGHT,
    YELLOW, GREEN,
    FONT_NAME, FONT_TITLE_SIZE, FONT_TIMER_SIZE, FONT_CHECKS_SIZE,
    TICK_MS,
)


class Display:
    """Owns the Tk root window and every widget.

    All application logic lives in the callbacks passed to __init__.
    Display never imports from timer.py and never makes decisions about
    session sequencing.
    """

    def __init__(
        self,
        tomato_path: Path,
        on_start: Callable[[], None],
        on_reset: Callable[[], None],
        on_tick_complete: Callable[[], None],
    ) -> None:
        self._on_start = on_start
        self._on_reset = on_reset
        self._on_tick_complete = on_tick_complete
        self._timer_id: str | None = None

        self.root = Tk()
        self.root.title(WINDOW_TITLE)
        self.root.config(padx=WINDOW_PAD_X, pady=WINDOW_PAD_Y, bg=YELLOW)

        self._build_widgets(tomato_path)
        self.root.focus_set()

    # ── Widget construction ────────────────────────────────────────────────────

    def _build_widgets(self, tomato_path: Path) -> None:
        self._title_label = Label(
            self.root,
            text="Timer",
            fg=GREEN,
            bg=YELLOW,
            font=(FONT_NAME, FONT_TITLE_SIZE),
        )
        self._title_label.grid(column=1, row=0)

        self._canvas = Canvas(
            self.root,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=YELLOW,
            highlightthickness=0,
        )
        self._tomato_img = PhotoImage(file=str(tomato_path))
        self._canvas.create_image(
            CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, image=self._tomato_img
        )
        self._timer_text = self._canvas.create_text(
            CANVAS_WIDTH // 2,
            130,
            text="00:00",
            fill="white",
            font=(FONT_NAME, FONT_TIMER_SIZE, "bold"),
        )
        self._canvas.grid(column=1, row=1)

        self._start_button = Button(
            self.root,
            text="Start",
            highlightthickness=0,
            command=self._on_start,
        )
        self._start_button.grid(column=0, row=2)

        self._reset_button = Button(
            self.root,
            text="Reset",
            highlightthickness=0,
            command=self._on_reset,
        )
        self._reset_button.grid(column=2, row=2)

        self._checkmarks_label = Label(
            self.root,
            fg=GREEN,
            bg=YELLOW,
            font=(FONT_NAME, FONT_CHECKS_SIZE),
        )
        self._checkmarks_label.grid(column=1, row=3)

    # ── Countdown management ───────────────────────────────────────────────────

    def start_countdown(self, seconds: int) -> None:
        """Begin a new countdown from `seconds`."""
        self._tick(seconds)

    def stop_countdown(self) -> None:
        """Cancel any running countdown without firing on_tick_complete."""
        if self._timer_id is not None:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None

    def _tick(self, count: int) -> None:
        minutes = count // 60
        seconds = count % 60
        self.render_timer(f"{minutes}:{seconds:02d}")
        if count > 0:
            self._timer_id = self.root.after(TICK_MS, self._tick, count - 1)
        else:
            self._timer_id = None
            self._on_tick_complete()

    # ── Render helpers ─────────────────────────────────────────────────────────

    def render_timer(self, text: str) -> None:
        """Update the countdown text on the canvas."""
        self._canvas.itemconfig(self._timer_text, text=text)

    def render_title(self, text: str, color: str) -> None:
        """Update the session-type label (e.g. "Work" / "Break")."""
        self._title_label.config(text=text, fg=color)

    def render_checkmarks(self, text: str) -> None:
        """Update the completed-session checkmark row."""
        self._checkmarks_label.config(text=text)

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def close(self) -> None:
        """Exit the application cleanly."""
        sys.exit(0)
