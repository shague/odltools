import unittest
import itm_state
from models import Model
from itm_state import DpnEndpoints


ip = "127.0.0.1"
port = "8080"


class TestItmState(unittest.TestCase):
    def setUp(self):
        self.dpn_endpoints = itm_state.DpnEndpoints(self, DpnEndpoints.container, Model.config, ip, port, 1)
        self.data = self.dpn_endpoints.get_from_file("itm-state_dpn-endpoints.json")

    def test_get_from_file(self):
        print "dpn-endpoints: {}".format(self.data)
        print "dpn-endpoints: \n{}".format(self.dpn_endpoints.pretty_format(self.data))

    def test_get_ip_address(self):
        dpn_ids = self.dpn_endpoints.get_dpn_ids()
        dpn_id = dpn_ids[0]
        ip_address = self.dpn_endpoints.get_ip_address(dpn_id)
        print "dpn_id: {}, ip_address: {}".format(dpn_id, ip_address)

    def test_get_all(self):
        print "dpn-endpoints: {}".format(self.data)
        print "dpn-endpoints: \n{}".format(self.dpn_endpoints.pretty_format(self.data))

        dpn_ids = self.dpn_endpoints.get_dpn_ids()
        dpn_id = dpn_ids[0]
        dpn_teps_info = self.dpn_endpoints.get_dpn_teps_info(dpn_id)
        print "dpn_teps_info for {}: {}".format(dpn_id, dpn_teps_info)

        ip_address = self.dpn_endpoints.get_ip_address(dpn_id)
        print "ip_address: {}".format(ip_address)

        self.get_info(DpnEndpoints.container)
        self.get_info(DpnEndpoints.dpn_teps_info)
        self.get_info(DpnEndpoints.tunnel_end_points)
        self.get_info(DpnEndpoints.dpn_id)

    def get_info(self, key):
        info = self.dpn_endpoints.get_kv(key, self.data, values=[])
        print "dpn info for {}: {}".format(key, info)
        return info

if __name__ == '__main__':
    unittest.main()
