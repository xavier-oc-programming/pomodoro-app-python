import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import GREEN
from timer import PomodoroTimer
from display import Display


def main() -> None:
    tomato_path = Path(__file__).parent / "tomato.png"
    pomodoro = PomodoroTimer()

    def handle_start() -> None:
        duration, title, color = pomodoro.advance()
        display.render_title(title, color)
        display.start_countdown(duration)

    def handle_tick_complete() -> None:
        display.render_checkmarks(pomodoro.checkmarks)
        handle_start()

    def handle_reset() -> None:
        pomodoro.reset()
        display.stop_countdown()
        display.render_timer("00:00")
        display.render_title("Timer", GREEN)
        display.render_checkmarks("")

    display = Display(
        tomato_path=tomato_path,
        on_start=handle_start,
        on_reset=handle_reset,
        on_tick_complete=handle_tick_complete,
    )

    display.root.mainloop()


if __name__ == "__main__":
    main()
