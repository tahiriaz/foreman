import os
import sys
import threading
import traceback
from contextlib import contextmanager
from datetime import datetime

from functions import vars


class TeeStream:
    """Write the same output to multiple streams."""

    def __init__(self, *streams):
        self.streams = streams
        self.lock = threading.RLock()

    def write(self, data):
        with self.lock:
            for stream in self.streams:
                stream.write(data)
                stream.flush()
        return len(data)

    def flush(self):
        with self.lock:
            for stream in self.streams:
                stream.flush()

    def isatty(self):
        return any(
            getattr(stream, "isatty", lambda: False)()
            for stream in self.streams
        )


@contextmanager
def capture_console_output(log_dir=None):
    """Mirror stdout/stderr to a timestamped UTF-8 log file."""
    if log_dir is None:
        log_dir = vars.LOG_DIR

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(
        log_dir,
        "{}_{}.log".format(vars.LOG_FILE_PREFIX, timestamp),
    )

    original_stdout = sys.stdout
    original_stderr = sys.stderr

    with open(log_path, "a", encoding="utf-8", buffering=1) as log_file:
        sys.stdout = TeeStream(original_stdout, log_file)
        sys.stderr = TeeStream(original_stderr, log_file)

        try:
            print("=" * 100)
            print("PROVISIONING LOG STARTED: {}".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            print("LOG FILE: {}".format(log_path))
            print("=" * 100)
            yield log_path
        except Exception:
            print("\nUNHANDLED EXCEPTION")
            print("=" * 100)
            traceback.print_exc()
            raise
        finally:
            print("=" * 100)
            print("PROVISIONING LOG ENDED: {}".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            print("=" * 100)
            sys.stdout.flush()
            sys.stderr.flush()
            sys.stdout = original_stdout
            sys.stderr = original_stderr