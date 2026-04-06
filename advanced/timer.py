import math

from config import (
    GREEN, PINK, RED,
    WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN,
    LONG_BREAK_EVERY, SHORT_BREAK_MODULO,
)


class PomodoroTimer:
    """Pure session-sequencing logic — no tkinter, no UI, no print()."""

    def __init__(self) -> None:
        self._reps: int = 0

    # ── Public API ─────────────────────────────────────────────────────────────

    def advance(self) -> tuple[int, str, str]:
        """Increment reps and return (duration_sec, title_text, title_colour).

        Called once per session start (including auto-advance after a countdown
        completes).  The caller is responsible for updating the UI with the
        returned values.
        """
        self._reps += 1
        if self._reps % LONG_BREAK_EVERY == 0:
            return (LONG_BREAK_MIN * 60, "Break", RED)
        elif self._reps % SHORT_BREAK_MODULO == 0:
            return (SHORT_BREAK_MIN * 60, "Break", PINK)
        else:
            return (WORK_MIN * 60, "Work", GREEN)

    def reset(self) -> None:
        """Reset session counter to zero."""
        self._reps = 0

    @property
    def checkmarks(self) -> str:
        """Return one ✔ per completed work session."""
        work_sessions = math.floor(self._reps / 2)
        return "✔" * work_sessions
