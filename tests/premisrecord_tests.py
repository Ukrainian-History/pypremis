import unittest
from pypremis.nodes import *
from pypremis.lib import PremisRecord
import pypremis.lib as pypremislib


class ImportTestCase(unittest.TestCase):
    """Functional tests for XML file import

    Uses the file "kitchen-sink.xml" as input, which is assumed to reside in the current working directory.
    Therefore, these tests should be run while in the 'tests' directory.

    """

    def setUp(self):
        """Import the 'kitchen-sink' XML file"""

        global kitchen_sink
        kitchen_sink = PremisRecord(frompath='kitchen-sink.xml')

    def test_event_count(self):
        self.assertTrue(len(kitchen_sink.get_event_list()) == 23)

    def test_object_count(self):
        self.assertTrue(len(kitchen_sink.get_object_list()) == 2)

    def test_agent_count(self):
        self.assertTrue(len(kitchen_sink.get_agent_list()) == 3)

    def test_rights_count(self):
        self.assertTrue(len(kitchen_sink.get_rights_list()) == 1)


class PremisRecordTestCase(unittest.TestCase):
    """Miscellaneous tests for PremisRecord
    """

    def test_duplicate_identifier_fails(self):
        identifier = EventIdentifier("stupid", "1")
        event_one = Event(identifier, "something", "now")
        event_two = Event(identifier, "something else", "later")
        with self.assertRaises(pypremislib.DuplicateIdentifierError):
            PremisRecord(events=[event_one, event_two])


if __name__ == '__main__':
    unittest.main()
