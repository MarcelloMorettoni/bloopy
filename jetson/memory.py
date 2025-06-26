"""Simple conversation memory storage for Bloopy."""

from pathlib import Path
from typing import List


class ConversationMemory:
    """Stores conversation history in a text file."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.touch(exist_ok=True)

    def append(self, line: str) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def load(self) -> List[str]:
        with self.path.open("r", encoding="utf-8") as f:
            return [l.rstrip("\n") for l in f]
