"""Entry point for the Raspberry Pi eye display."""

from pathlib import Path
import shutil

# For now we reuse the standalone script located at the repository root.
# This wrapper simply executes that script so users can run
# ``python -m raspberry.eyes`` from the Pi.

HERE = Path(__file__).resolve().parent
script = HERE.parent / "full_eyes.py"

if __name__ == "__main__":
    # Execute the script in the current interpreter
    globals_dict = {
        "__file__": str(script),
        "__name__": "__main__",
    }
    with open(script, "r", encoding="utf-8") as f:
        code = compile(f.read(), str(script), "exec")
        exec(code, globals_dict)
