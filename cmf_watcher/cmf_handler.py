import glob
import hashlib
import logging
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
# Imported in this manner so that there is a clear distingtion in this file between
# `hum_event.Event` and `fs_event`
import mapactionpy_controller.event as hum_event
import os
from watchdog.events import RegexMatchingEventHandler, PatternMatchingEventHandler
import take_action
import time


class CrashMoveFolderHandler(PatternMatchingEventHandler):
    # files_in_root_pattrn
    # individual_files_pattrn
    # dir_pattrn


    def __init__(self, description_file):
        self.cmf, self.hum_event = self.parse_input_path(description_file)
        self._get_file_patterns_from_cmf_description(self.cmf)

        files_patterns = self.files_in_root_pattrn + \
                         self.discrete_files_pattrn + \
                         self.shpfile_dir_pattrn + \
                         self.gdb_list_pattrn

        logging.debug("files_patterns={}".format(files_patterns))
        print("files_patterns={}".format(files_patterns))
        super().__init__(files_patterns, ignore_patterns=self.ignore_dir_pattrn)


    def _get_file_patterns_from_cmf_description(self, cmf):
        # root dir
        self.files_in_root_pattrn = [cmf.path + os.sep + r"*.json"]

        # Files to watch. There are various files which should be watched
        # individually, including directories containing many of them. The paths
        # for these files and/or their directories are add to `discrete_files`
        # T
        # 5 files (alphabeltical order just for readablity)
        self.discrete_files_pattrn = []
        self.discrete_files_pattrn.append(cmf.data_nc_definition)
        self.discrete_files_pattrn.append(cmf.layer_nc_definition)
        self.discrete_files_pattrn.append(cmf.layer_properties)
        self.discrete_files_pattrn.append(cmf.map_definitions)
        self.discrete_files_pattrn.append(cmf.mxd_nc_definition)
        # 4 directories which contain discrete files
        self.discrete_files_pattrn.append(cmf.layer_rendering + os.sep + r"*")
        self.discrete_files_pattrn.append(cmf.mxd_templates + os.sep + r"*")
        self.discrete_files_pattrn.append(cmf.mxd_products + os.sep + r"*")
        self.discrete_files_pattrn.append(cmf.qgis_templates + os.sep + r"*")

        # Geodata to watch
        # Shapefiles and Geodatabases consistant of multiple OS files. 
        self.shpfile_dir_pattrn = []
        self.shpfile_dir_pattrn.append(cmf.active_data + os.sep + r"*")
        # We need to go one level deep with the Active Data directory for shapefiles
        self.shpfile_dir_pattrn.append(cmf.active_data + os.sep + r"*" + os.sep + r"*")
        # We need to go two levels deep with the Active Data directory for shapefiles
        self.gdb_list_pattrn = []
        self.gdb_list_pattrn.append(cmf.active_data + os.sep + r"*.gdb" + os.sep + r"**")
        self.gdb_list_pattrn.append(cmf.active_data + os.sep + r"*" + os.sep + r"*.gdb" + os.sep + r"**")

        # We can safely ignore changes to these directories
        #     `cmf.original_data`
        #     `cmf.export_dir`
        self.ignore_dir_pattrn = []
        self.ignore_dir_pattrn.append(cmf.original_data + os.sep + r"*")
        self.ignore_dir_pattrn.append(cmf.export_dir + os.sep + r"*")

        # return (files_in_root, discrete_files, geodata_dir_list, ignore_dir_list)


    def parse_input_path(self, description_file):
        """
        The input file should be either:
            a) the path to a cmf_description.json file
            b) the path to an event_description.json

        Returns:
            If `json_file` is a path to an event_description.json file, returns a tuple of the
            `CrashMoveFolder` object and the `Event` object.
            If `json_file` is a path to a cmf_description.json file, returns a tuple of the 
            `CrashMoveFolder` object and `None` to represent the Event.

        Anything that doesn't load into one or other of those classes will result in a `ValueError`
        being thrown.
        """
        try:
            e = hum_event.Event(description_file)
            cmf = CrashMoveFolder(e.cmf_descriptor_path, verify_on_creation=True)
            print("found both event and cmf descriptions")
            return cmf, e
        except (ValueError, KeyError, TypeError):
            pass

        try:
            cmf = CrashMoveFolder(description_file, verify_on_creation=True)
            print("found cmf description but not event description")
            return cmf, None
        except (ValueError, KeyError, TypeError):
            pass

        # If we've got this far then we have a value error.
        # Need to handle the 
        return None, None

    def on_any_event(self, event):
        self.process_event(event)


    def process_event(self, event):

        if self._match_event_src_file_name(event, self.files_in_root_pattrn):
            print("found change to root files")
            self._wait_for_stablity([event.src_path])
            # Chech that the changed 
            cmf, ev = self.parse_input_path(event.src_path)
            if cmf:
                self.cmf, self.ev = cmf, ev
            self._get_file_patterns_from_cmf_description(self.cmf)

        elif self._match_event_src_file_name(event, self.discrete_files_pattrn):
            print("found change to discrete files")
            self._wait_for_stablity([event.src_path])

        elif self._match_event_src_file_name(event, self.shpfile_dir_pattrn):
            print("found change to shapefiles")
            f_list = self._get_shapefile_filelist(event)
            self._wait_for_stablity(f_list)

        elif self._match_event_src_file_name(event, self.gdb_list_pattrn):
            print("found change to GeoDBs")
            f_list = self._get_shapefile_filelist(event)
            self._wait_for_stablity(f_list)

        take_action.process(event)


    def _get_shapefile_filelist(self, event):
        """
        Works for any collection of files which are:
        a) in the same directory
        b) share a common basename, but have different extensions
        Assumed the caller has already established that the filechange event
        relates to a shapefile.
        """
        pattern = os.path.splitext(event.src_path)[0]
        pattern = pattern + r".*"
        f_list = glob.glob(pattern)
        # print("_get_shapefile_filelist, f_list={}".format(f_list))
        return f_list

    def _get_gdb_filelist(self):
        pass

    def _match_event_src_file_name(self, event, ptn_list):
        src_name = os.path.realpath(os.path.normpath(event.src_path))
        for pattern in ptn_list:
            matched_files = glob.glob(pattern)
            matched_files = map(os.path.normcase, matched_files)
            matched_files = map(os.path.realpath, matched_files)
            for fn in matched_files:
                if os.path.samefile(fn, src_name):
                    return src_name
        
        return None


    def _wait_for_stablity(self, f_list):
        # print('_wait_for_stablity f_list={}'.format(f_list))
        old_hash_value = -1, -1
        new_hash_value = self._hash_files(f_list)
        while old_hash_value[0] != new_hash_value[0]:
            # print(old_hash_value, new_hash_value, f_list)
            min_delay = 0.1
            if (2*new_hash_value[1]) > min_delay:
                delay = 2*new_hash_value[1]
            else:
                delay = min_delay

            # print("sleep for {} second".format(delay))
            time.sleep(delay)
            old_hash_value = new_hash_value
            new_hash_value = self._hash_files(f_list)
     

    def _hash_files(self, f_list):
        """
        Calculates the MD5 has of one or more files.

        The list of files is sorted before the has if calculated.

        Returns a tuple. First element is the md5 hash of the file(s). The secound
        element is the time (in absolute secounds) to calculate the hash.  
        """
        starttime = time.time()
        BLOCKSIZE = 65536
        hasher = hashlib.md5()
        # print('unsorted f_list {}'.format(f_list))
        f_list.sort()
        # print('sorted f_list {}'.format(f_list))
        for fn in f_list:
            if os.path.isfile(fn):
                with open(fn, 'rb') as afile:
                    buf = afile.read(BLOCKSIZE)
                    while len(buf) > 0:
                        hasher.update(buf)
                        buf = afile.read(BLOCKSIZE)

        return hasher.hexdigest(), time.time() - starttime
