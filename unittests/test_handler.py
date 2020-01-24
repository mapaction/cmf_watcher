from unittest import TestCase

class TestCMFHandler(TestCase):

    def setUp(self):
        pass

    def test_get_file_patterns_from_cmf_description(self):
        self.fail()

    def test_parse_input_path(self):
        """
            Need to handle the cases
            a) Not a valid Event file
            b) A valid Event file, but a corrupt cmf file
            c) A valid Event file and a valid cmf file, but the cmf paths aren't valid
            d) Everything valid
        """
        self.fail()

    def test_change_to_root_files(self):
        """
            Need to handle the cases
            b) multiple event files
            c) multiple cmf files
            d) removal of existing event file
            e) removal of existing cmf file
            f) cooruption of existing event file
            g) cooruption of existing cmf file
            h) new or modified json file with is unrelated to either a cmf or event file
        """
        self.fail()

    def test_change_to_descrete_files(self):
        """
            Need to handle the cases
            a) amend to one of the named files
            b) delete one of the named files
            c) add new file to one of the named dirs
            d) admend file to one of the named dirs
            e) remove file from one of the named dirs
        """
        self.fail()

    def test_change_to_shapefiles(self):
        self.fail()

    def test_change_to_gdb(self):
        self.fail()

    def test_hash_single_file(self):
        self.fail()

    def test_hash_multiple_files(self):
        """
        Need to test:
            a) list of files in same directory given in alphabetical order
            b) list of files in same directory given in non-alphabetical order
            c) list of files in different directories given in alphabetical order
            d) list of files in different directories given in non-alphabetical order
            e) list of files zero length files
            f) list including the same file(s) multiple times
            g) list including directories
            h) list including non-existant files
            i) shapefile-specific things relating to lock files
            j) file-geodatabase-specific things relating to lock files
        """
        self.fail()
