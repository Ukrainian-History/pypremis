import unittest
from pypremis.nodes import *
from pypremis.lib import PremisRecord

"""Functional/integrative tests for XML file import

Uses the file "kitchen-sink.xml" as input, which is assumed to reside in the current working directory.
Therefore, these tests should be run while in the 'tests' directory.

"""


class PypremisImportTestCase(unittest.TestCase):
    def setUp(self):
        """Import the 'kitchen-sink' XML file"""

        global kitchen_sink
        kitchen_sink = PremisRecord(frompath='kitchen-sink.xml')

    def test_event_import(self):
        self.assertTrue(len(kitchen_sink.get_event_list()) == 24)

    def test_object_import(self):
        pass

    def test_agent_import(self):
        pass

    def test_rights_import(self):
        pass


if __name__ == '__main__':
    unittest.main()
