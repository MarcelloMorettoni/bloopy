from __future__ import annotations

import threading
import time
from pathlib import Path

from jetson.plugin import BloopyPlugin
from jetson.servo_api import CHANNELS, ServoCommand, move_servos


class WaveHiPlugin(BloopyPlugin):
    """Wave and show happy eyes when the user says hello."""

    name = "wave_hi"

    def run(self) -> None:  # pragma: no cover - plugin runs forever
        thread = threading.Thread(target=self._watch_loop, daemon=True)
        thread.start()

    def _watch_loop(self) -> None:
        log = Path("conversation.log")
        log.touch(exist_ok=True)
        position = log.stat().st_size
        while True:
            with log.open("r", encoding="utf-8") as f:
                f.seek(position)
                lines = f.readlines()
                if lines:
                    position = f.tell()
                for line in lines:
                    lower = line.lower()
                    if lower.startswith("you:") and ("hi" in lower or "hello" in lower):
                        self._wave_and_smile()
            time.sleep(0.5)

    def _wave_and_smile(self) -> None:
        sequence = [
            ServoCommand(channel=CHANNELS["shoulder_lift"], angle=45),
            ServoCommand(channel=CHANNELS["elbow"], angle=90),
        ]
        move_servos(sequence)
        for _ in range(2):
            move_servos([ServoCommand(channel=CHANNELS["wrist"], angle=30)])
            time.sleep(0.3)
            move_servos([ServoCommand(channel=CHANNELS["wrist"], angle=-30)])
            time.sleep(0.3)
        move_servos([
            ServoCommand(channel=CHANNELS["wrist"], angle=0),
            ServoCommand(channel=CHANNELS["elbow"], angle=0),
            ServoCommand(channel=CHANNELS["shoulder_lift"], angle=0),
        ])
        Path("eye_command.txt").write_text("happy\n", encoding="utf-8")
