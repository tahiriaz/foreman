import sys
import traceback

from functions import vars
from functions.output_log import capture_console_output


def main():
    with capture_console_output() as log_path:
        try:
            from functions.orchestrator import provision_from_excel

            print("Python executable : {}".format(sys.executable))
            print("Project directory : {}".format(vars.PROJECT_DIR))
            print("Templates directory: {}".format(vars.TEMPLATES_DIR))
            print("Resource list     : {}".format(vars.RESOURCE_LIST))
            print("Sheet             : {}".format(vars.SHEET_NAME))
            print("Rows              : {} through {}".format(
                vars.START_ROW,
                vars.END_ROW,
            ))
            print("Parallel workers  : {}".format(vars.MAX_WORKERS))
            print("Foreman creates   : {}".format(
                vars.FOREMAN_CREATE_CONCURRENCY
            ))
            print("Log file          : {}".format(log_path))
            print()

            provision_from_excel()
            return 0

        except Exception:
            print("\nFATAL ERROR")
            print("=" * 100)
            traceback.print_exc()
            return 1


if __name__ == "__main__":
    sys.exit(main())
