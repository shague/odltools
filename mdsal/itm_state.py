from models import Model


name = "itm-state"


class DpnEndpoints(Model):
    container = "dpn-endpoints"
    dpn_teps_info = "DPN-TEPs-info"
    dpn_id = "DPN-ID"
    tunnel_end_points = "tunnel-end-points"
    ip_address = "ip-address"

    def item_generator(self, json_input, lookup_key):
        if isinstance(json_input, dict):
            for k, v in json_input.iteritems():
                if k == lookup_key:
                    yield v
                else:
                    for child_val in self.item_generator(v, lookup_key):
                        yield child_val
        elif isinstance(json_input, list):
            for item in json_input:
                for item_val in self.item_generator(item, lookup_key):
                    yield item_val

    def get_dpn_teps_infos(self):
        return self.data[self.container][self.dpn_teps_info]

    def get_dpn_teps_info(self, dpn_id):
        dpn_teps_infos = self.get_dpn_teps_infos()
        for dpn_teps_info in dpn_teps_infos:
            if dpn_teps_info[self.dpn_id] == dpn_id:
                return dpn_teps_info

    def get_tunnel_endpoints(self, dpn_id):
        dpn_teps_infos = self.get_dpn_teps_infos()
        for dpn_teps_info in dpn_teps_infos:
            if dpn_teps_info[self.dpn_id] == dpn_id:
                return dpn_teps_info[self.tunnel_end_points]

    def get_dpn_ids(self):
        return self.get_kv(DpnEndpoints.dpn_id, self.data, values=[])

    def get_ip_address(self, dpn_id):
        tunnel_endpoints = self.get_tunnel_endpoints(dpn_id)
        return tunnel_endpoints[0][self.ip_address]


def dpn_endpoints(store, ip, port, debug=0):
    return DpnEndpoints(name, DpnEndpoints.container, store, ip, port, debug)
