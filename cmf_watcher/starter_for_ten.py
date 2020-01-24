
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler, RegexMatchingEventHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # event_handler = LoggingEventHandler()
    event_handler = PatternMatchingEventHandler(patterns="*.json")
    # event_handler = RegexMatchingEventHandler(regexes=['.+json'])
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

###################
# Has a shapefile changed?
###################
# Check the hashes of a shapefile
# https: // stackoverflow.com/a/34919942


################
# Do I have either an Event Description or a CMF Description?
################
# parameters
# D:\MapAction or
# ...\..\..\. On FileServer

# If "D:\MapAction"
# Search for "**\*.json"


##############
# Do I have an Event too?
##############


################
# I have CMF without an event
################


################
# I have CMF and Event 
################



