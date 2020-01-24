# cmf_watcher
 
CrashMoveFolderWatcher class
 - Takes the path to a `cmf_descriptor` file (or an `event_descriptor` file) and watches changes
 - If instainicated with a `cmf_descripitor` and not an event descriptor, it will look for all new json files within the root and see if they validate as an Event object.


CrashMoveFolderHandler class
 - Responses to events within a CMF, using the information in the  `cmf_descriptor` and `event_descriptor` files, to make appropriate actions accordingly
 - This class is typically responsile for making calls to the GoCD API



CMFfinder
 - A handler. When a new CMF is detected (as per NewCMFWatcher) this handler starts a new CrashMoveFolderWatcher class.


NewCMFWatcher
- Watches a directory (on a laptop (D:\MapAction) or file server) for the appearance of new CMF directories - ie any directory with:
  - a json that loads as a cmf_descriptor object
  - all of the paths in that cmf_descriptor object are valid



# Mode A - directly watching a specfic cmf:
crash_move_folder_watcher
 - watch <path-to-cmf-description.json | path-to-event-description.json>
 - gocd-config-stuff 

# Mode B - hunting for cmfs
crash_move_folder_watcher
 - search <path-to-root-dir>
 - gocd-config-stuff 



# Notes and references:
#
# https://pythonhosted.org/watchdog/api.html  # event-handler-classes
# https://pypi.org/project/watchdog/
# https://github.com/gorakhargosh/watchdog/issues/577
# https://github.com/gorakhargosh/watchdog/issues/391
# https://blog.magrathealabs.com/filesystem-events-monitoring-with-python-9f5329b651c3
# https://stackoverflow.com/questions/44713742/python-trigger-file-change-events
# 
# GoCD client:
# This GoCD Python client looks the most promising:
# https://github.com/grundic/yagocd
# https://yagocd.readthedocs.io/en/latest/readme.html#different-implementations-of-gocd-api
