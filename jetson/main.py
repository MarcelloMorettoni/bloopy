"""Entry point for Bloopy running on the Jetson Orin."""

from pathlib import Path

from .memory import ConversationMemory
from .plugin import PluginManager
from .servo_api import CHANNELS, ServoCommand, move_servos


MEMORY_FILE = Path("conversation.log")
PLUGIN_DIR = Path("plugins")


def main() -> None:
    memory = ConversationMemory(MEMORY_FILE)
    manager = PluginManager(PLUGIN_DIR)
    manager.load_plugins()

    # Example: move neck to neutral position on startup
    move_servos([
        ServoCommand(channel=CHANNELS["neck_yaw"], angle=0),
        ServoCommand(channel=CHANNELS["neck_pitch"], angle=0),
    ])

    # Run all loaded plugins (non-blocking tasks)
    manager.run_all()

    # Placeholder REPL loop for conversation
    try:
        while True:
            text = input("You: ")
            if not text:
                continue
            memory.append(f"You: {text}")
            # Echo back for now
            response = f"Bloopy heard: {text}"
            print(response)
            memory.append(response)
    except KeyboardInterrupt:
        print("Exiting")


if __name__ == "__main__":
    main()
