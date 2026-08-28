import logging
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


def _iter_loggers():
    """Yield all instantiated logging.Logger objects, including root."""
    yield logging.getLogger()

    for logger_obj in logging.Logger.manager.loggerDict.values():
        if isinstance(logger_obj, logging.Logger):
            yield logger_obj


def _rebind_logging_streams(original_stdout, original_stderr):
    """
    Rebind pre-existing StreamHandlers to the tee streams.

    Some project scripts create logging.StreamHandler(sys.stdout) during module
    import. Without rebinding, those handlers would bypass console capture when
    capture_console_output() starts later from the entry point.
    """
    changed = []

    for logger_obj in _iter_loggers():
        for handler in logger_obj.handlers:
            if isinstance(handler, logging.FileHandler):
                continue

            if not isinstance(handler, logging.StreamHandler):
                continue

            stream = getattr(handler, "stream", None)

            if stream is original_stdout:
                changed.append((handler, stream))
                handler.stream = sys.stdout
            elif stream is original_stderr:
                changed.append((handler, stream))
                handler.stream = sys.stderr

    return changed


@contextmanager
def capture_console_output(
    log_dir=None,
    log_prefix=None,
    title=None,
):
    """Mirror stdout/stderr to a timestamped UTF-8 console log file."""
    if log_dir is None:
        log_dir = vars.LOG_DIR

    if log_prefix is None:
        log_prefix = vars.LOG_FILE_PREFIX

    if title is None:
        title = "SCRIPT EXECUTION"

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = os.path.join(
        log_dir,
        "{}_{}.log".format(log_prefix, timestamp),
    )

    original_stdout = sys.stdout
    original_stderr = sys.stderr
    rebound_handlers = []

    with open(log_path, "a", encoding="utf-8", buffering=1) as log_file:
        sys.stdout = TeeStream(original_stdout, log_file)
        sys.stderr = TeeStream(original_stderr, log_file)
        rebound_handlers = _rebind_logging_streams(
            original_stdout,
            original_stderr,
        )

        try:
            print("=" * 100)
            print("{} STARTED: {}".format(
                title,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ))
            print("CONSOLE LOG: {}".format(log_path))
            print("=" * 100)
            yield log_path
        except Exception:
            print("\nUNHANDLED EXCEPTION")
            print("=" * 100)
            traceback.print_exc()
            raise
        finally:
            print("=" * 100)
            print("{} ENDED: {}".format(
                title,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ))
            print("=" * 100)

            try:
                sys.stdout.flush()
                sys.stderr.flush()
            except Exception:
                pass

            for handler, original_stream in rebound_handlers:
                try:
                    handler.stream = original_stream
                except Exception:
                    pass

            sys.stdout = original_stdout
            sys.stderr = original_stderr


def run_logged_main(
    main_func,
    log_prefix=None,
    title=None,
    log_dir=None,
):
    """Run a script main() inside standardized console logging."""
    with capture_console_output(
        log_dir=log_dir,
        log_prefix=log_prefix,
        title=title,
    ):
        try:
            result = main_func()
        except SystemExit as exc:
            code = exc.code

            if code is None:
                return 0

            try:
                return int(code)
            except Exception:
                return 1
        except Exception:
            print("\nFATAL ERROR")
            print("=" * 100)
            traceback.print_exc()
            return 1

    if result is None:
        return 0

    try:
        return int(result)
    except Exception:
        return 0
