"""Servo control API for Bloopy using RT robot 32 interface.

This module defines the channel mappings for the robot and provides a
placeholder API for sending movement commands to the servos connected to the
Jetson Orin. Actual communication with the hardware should be implemented
by replacing the ``send_command`` function with calls to the RT robot 32
library or protocol.
"""

from dataclasses import dataclass
from typing import Dict, Iterable

# Channel mapping based on physical configuration
CHANNELS: Dict[str, int] = {
    "neck_yaw": 1,
    "neck_pitch": 2,
    "shoulder_rotate": 3,
    "shoulder_lift": 4,
    "bicep": 5,
    "elbow": 6,
    "forearm": 7,
    "wrist": 8,
    "thumb": 9,
    "index": 10,
    "middle": 11,
    "ring": 12,
    "pinky": 13,
}

@dataclass
class ServoCommand:
    """Represents a command for a single servo."""

    channel: int
    angle: float
    duration: float = 0.5  # seconds


def send_command(cmd: ServoCommand) -> None:
    """Send a command to a servo.

    This implementation is a stub that only logs the command. Replace this
    with communication code for the RT robot 32 interface when running on the
    Jetson Orin.
    """
    print(f"[SERVO] Channel {cmd.channel} -> angle={cmd.angle} dur={cmd.duration}")


def move_servos(commands: Iterable[ServoCommand]) -> None:
    """Send multiple commands sequentially."""
    for cmd in commands:
        send_command(cmd)
