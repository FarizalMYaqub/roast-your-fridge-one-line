"""One line that roasts my fridge, written to the make.fun output file."""

import os
import sys

# The roast. One line, about the fridge, built on one specific habit of
# it: the door alarm that starts beeping after a few seconds open, as if
# the fridge were the one worried about the electricity bill. The twist
# lands in the last clause: the fridge is not paying the bill, it is
# most of the bill.
ROAST = (
    "My fridge beeps if I leave the door open ten seconds, "
    "like it's the one paying the electric bill — buddy, "
    "you are the electric bill."
)

MAX_CHARS = 200
FILE_NAME = "entry.txt"


def output_dir():
    """Where the harness expects the entry: MAKEFUN_OUTPUT_DIR or /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def check_line(line):
    """Fail loudly rather than write an entry the gate would reject."""
    if not line.strip():
        raise ValueError("roast is empty")
    if "\n" in line or "\r" in line:
        raise ValueError("roast must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"roast is {len(line)} chars, limit is {MAX_CHARS}")
    if "fridge" not in line.lower():
        raise ValueError("roast must actually be about the fridge")


def tidy(line):
    """Collapse any accidental double spaces so the line reads cleanly."""
    return " ".join(line.split())


def write_entry(line, directory):
    """Write the line atomically, then read it back to prove it landed."""
    os.makedirs(directory, exist_ok=True)
    target = os.path.join(directory, FILE_NAME)
    staging = target + ".tmp"
    with open(staging, "w", encoding="utf-8") as handle:
        handle.write(line)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(staging, target)
    with open(target, encoding="utf-8") as handle:
        written = handle.read()
    if written != line:
        raise IOError("read-back does not match the roast that was written")
    return target


def main():
    line = tidy(ROAST)
    check_line(line)
    path = write_entry(line, output_dir())
    print(f"wrote {len(line)} chars to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
