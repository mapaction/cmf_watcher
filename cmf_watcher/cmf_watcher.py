import sys
import os
import time
import argparse

from watchdog.observers import Observer
from cmf_handler import CrashMoveFolderHandler


class CrashMoveFolderWatcher:
    def __init__(self, src_path):
        self.__src_path = os.path.dirname(src_path)
        self.__event_handler = CrashMoveFolderHandler(src_path)
        self.__event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )


def main():
    src_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    CrashMoveFolderWatcher(src_path).run()

def get_args():
    parser = argparse.ArgumentParser(
        description=('This tool checks the conformance with the naming-convention for selected'
                     'files within the Crash Move Folder')
    )
    parser.add_argument("cmf_config_path", help="path to layer directory", metavar="FILE",
                        type=lambda x: os.path.exists(x))

    return parser.parse_args()


if __name__ == "__main__":
    main()
