# Bloopy Robot

Bloopy is a personal companion robot composed of two main computing units:

- **Jetson Orin** – Handles motor control, audio processing and runs the core
  application.
- **Raspberry Pi 4** – Drives the eye display and can handle additional
  lightweight tasks.

This repository currently contains a prototype of the eye rendering software
and initial scaffolding for the Jetson application.

## Directory Layout

```
jetson/     Core modules executed on the Jetson Orin
raspberry/  Code for the Raspberry Pi eye display
plugins/    Example plugin directory
```

### `jetson/` Modules

- `servo_api.py` – Defines servo channel mappings and provides a stub API for
  issuing movement commands over the RT robot 32 interface.
- `plugin.py` – Lightweight plugin system so new behaviors can be dropped into
  the `plugins` folder and executed dynamically.
- `memory.py` – Very simple conversation memory backed by a text file.
- `main.py` – Example entry point bringing everything together.

### `raspberry/`

Contains code for the eye display. The existing `full_eyes.py` script can be
run directly on the Pi to show animated eyes using `pygame`.

## Servo Channel Mapping

The servos are connected via the RT robot 32 interface and mapped as follows:

| Channel | Function              |
| ------- | -------------------- |
| 1       | Neck yaw             |
| 2       | Neck pitch           |
| 3       | Left shoulder rotate |
| 4       | Left shoulder lift   |
| 5       | Bicep                |
| 6       | Elbow                |
| 7       | Forearm              |
| 8       | Wrist                |
| 9       | Thumb                |
| 10      | Index finger         |
| 11      | Middle finger        |
| 12      | Ring finger          |
| 13      | Pinky finger         |

Update `servo_api.py` if the wiring changes or more channels are added.

## Running

Install the requirements and run the main program. The Jetson unit expects
``ollama`` to be installed with the ``llama3.3`` model available. The
environment variable ``REMOTE_API_URL`` can optionally point to an external
LLM service which will be used if local inference fails.

```bash
pip install -r requirements.txt
python -m jetson.main
```

Plugins can be placed in the `plugins/` directory and will automatically be
loaded on startup.

### Example: Wave when greeted

The `WaveHiPlugin` monitors `conversation.log` for user messages. When it sees
"hi" or "hello" it performs a small wave with the arm and writes ``happy`` to
``eye_command.txt`` so the Raspberry Pi eye program can switch expressions.

```text
You: hi bloopy
[SERVO] Channel 4 -> angle=45 dur=0.5
...
```
