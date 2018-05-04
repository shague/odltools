import logging
import unittest
from odltools import logg
from odltools.netvirt import analyze
from odltools.netvirt import tests
from odltools.netvirt.tests import capture


class TestAnalyze(unittest.TestCase):
    # TODO: capture stdout and check for list of tables.

    def setUp(self):
        logg.Logger(logging.INFO, logging.INFO)
        self.args = tests.Args(path=tests.get_resources_path())

    @unittest.skip("skipping")
    def test_analyze_trunks(self):
        analyze.analyze_trunks(self.args)

    def test_analyze_interface(self):
        self.args.ifname = "98c2e265-b4f2-40a5-8f31-2fb5d2b2baf6"
        with capture.capture(analyze.analyze_interface, self.args) as output:
            self.assertTrue("98c2e265-b4f2-40a5-8f31-2fb5d2b2baf6" in output)

    def test_analyze_inventory(self):
        self.args.store = "config"
        self.args.nodeid = "132319289050514"
        with capture.capture(analyze.analyze_inventory, self.args) as output:
            self.assertTrue("132319289050514" in output)
        self.args.store = "operational"
        self.args.nodeid = "233201308854882"
        # not a great test, but there are no flows in the operational
        with capture.capture(analyze.analyze_inventory, self.args) as output:
            self.assertTrue("Inventory Operational" in output)


if __name__ == '__main__':
    unittest.main()
