# Copyright 2018 Red Hat, Inc. and others. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from odltools.netvirt import config
# from odltools.netvirt.config import gnodes
# from odltools.netvirt.config import gports
from odltools.netvirt import flow_parser
from odltools.netvirt import flows
from odltools.mdsal.models import constants
from odltools.mdsal.models.neutron import Neutron
from odltools.mdsal.models.opendaylight_inventory import Nodes
from odltools.mdsal.models.model import Model
from odltools.netvirt import utils


def print_keys(args, ifaces, ifstates):
    print("InterfaceNames: {}\n".format(utils.format_json(args, ifaces.keys())))
    print("IfStateNames: {}".format(utils.format_json(args, ifstates.keys())))


def by_ifname(args, ifname, ifstates, ifaces):
    config.get_models(args, {
        "itm_state_tunnels_state",
        "neutron_neutron"})
    ifstate = ifstates.get(ifname)
    iface = ifaces.get(ifname)
    port = None
    tunnel = None
    tun_state = None
    if iface and iface.get('type') == constants.IFTYPE_VLAN:
        ports = config.gmodels.neutron_neutron.get_objects_by_key(obj=Neutron.PORTS)
        port = ports.get(ifname)
    elif iface and iface.get('type') == constants.IFTYPE_TUNNEL:
        tun_states = config.gmodels.itm_state_tunnels_state.get_clist_by_key()
        tun_state = tun_states.get(ifname)
    else:
        print("UNSUPPORTED IfType")
    return iface, ifstate, port, tunnel, tun_state


def analyze_interface(args):
    config.get_models(args, {
        "ietf_interfaces_interfaces",
        "ietf_interfaces_interfaces_state"})
    ifaces = config.gmodels.ietf_interfaces_interfaces.get_clist_by_key()
    ifstates = config.gmodels.ietf_interfaces_interfaces_state.get_clist_by_key()

    if not args.ifname:
        print_keys(args, ifaces, ifstates)
        return

    ifname = args.ifname
    iface, ifstate, port, tunnel, tunState = by_ifname(args, ifname, ifstates, ifaces)
    print("InterfaceConfig: \n{}".format(utils.format_json(args, iface)))
    print("InterfaceState: \n{}".format(utils.format_json(args, ifstate)))
    if port:
        print("NeutronPort: \n{}".format(utils.format_json(args, port)))
        # analyze_neutron_port(port, iface, ifstate)
        return
    if tunnel:
        print("Tunnel: \n{}".format(utils.format_json(args, tunnel)))
    if tunState:
        print("TunState: \n{}".format(utils.format_json(args, tunState)))
    # if ifstate:
        # ncid = ifstate.get('lower-layer-if')[0]
        # nodeid = ncid[:ncid.rindex(':')]
        # analyze_inventory(nodeid, True, ncid, ifname)
        # analyze_inventory(nodeid, False, ncid, ifname)


def analyze_trunks(args):
    config.get_models(args, {
        "ietf_interfaces_interfaces",
        # "ietf_interfaces_interfaces_state",
        "l3vpn_vpn_interfaces",
        "neutron_neutron"})

    vpninterfaces = config.gmodels.l3vpn_vpn_interfaces.get_clist_by_key()
    ifaces = config.gmodels.ietf_interfaces_interfaces.get_clist_by_key()
    # ifstates = config.gmodels.ietf_interfaces_interfaces_state.get_clist_by_key()
    nports = config.gmodels.neutron_neutron.get_objects_by_key(obj=Neutron.PORTS)
    ntrunks = config.gmodels.neutron_neutron.get_trunks_by_key()
    subport_dict = {}
    for v in ntrunks.values():
        nport = nports.get(v.get('port-id'))
        s_subports = []
        for subport in v.get('sub-ports'):
            sport_id = subport.get('port-id')
            snport = nports.get(sport_id)
            svpniface = vpninterfaces.get(sport_id)
            siface = ifaces.get(sport_id)
            # sifstate = ifstates.get(sport_id)
            subport['SubNeutronPort'] = 'Correct' if snport else 'Wrong'
            subport['SubVpnInterface'] = 'Correct' if svpniface else 'Wrong'
            subport['ofport'] = Model.get_ofport_from_ncid()
            if siface:
                vlan_mode = siface.get('odl-interface:l2vlan-mode')
                parent_iface_id = siface.get('odl-interface:parent-interface')
                if vlan_mode != 'trunk-member':
                    subport['SubIface'] = 'WrongMode'
                elif parent_iface_id != v.get('port-id'):
                    subport['SubIface'] = 'WrongParent'
                elif siface.get('odl-interface:vlan-id') != subport.get('segmentation-id'):
                    subport['SubIface'] = 'WrongVlanId'
                else:
                    subport['SubIface'] = 'Correct'
            else:
                subport['SubIface'] = 'Wrong'
                # s_subport = 'SegId:{}, PortId:{}, SubNeutronPort:{}, SubIface:{}, SubVpnIface:{}'.format(
                #     subport.get('segmentation-id'), subport.get('port-id'),
                #     subport.get('SubNeutronPort'),
                #     subport.get('SubIface'),
                #     subport.get('SubVpnInterface'))
            s_subports.append(subport)
            subport_dict[subport['port-id']] = subport
            s_trunk = 'TrunkName:{}, TrunkId:{}, PortId:{}, NeutronPort:{}, SubPorts:{}'.format(
                v.get('name'), v.get('uuid'), v.get('port-id'),
                'Correct' if nport else 'Wrong', utils.format_json(args, s_subports))
            print(s_trunk)
            print("\n------------------------------------")
            print("Analyzing Flow status for SubPorts")
            print("------------------------------------")
            for flow in utils.sort(flows.get_all_flows(args, ['ifm'], ['vlanid']), 'ifname'):
                subport = subport_dict.get(flow.get('ifname')) or None
                vlanid = subport.get('segmentation-id') if subport else None
                ofport = subport.get('ofport') if subport else None
                flow_status = 'Okay'
                if flow.get('ofport') and flow.get('ofport') != ofport:
                    flow_status = 'OfPort mismatch for SubPort:{} and Flow:{}'.format(subport, flow.get('flow'))
                if flow.get('vlanid') and flow.get('vlanid') != vlanid:
                    flow_status = 'VlanId mismatch for SubPort:{} and Flow:{}'.format(subport, flow.get('flow'))
                if subport:
                    print("SubPort:{},Table:{},FlowStatus:{}".format(
                        subport.get('port-id'), flow.get('table'), flow_status))


def analyze_neutron_port(args, port, iface, ifstate):
    for flow in utils.sort(flows.get_all_flows(args, ['all']), 'table'):
        if ((flow.get('ifname') == port['uuid']) or
                (flow.get('lport') and ifstate and flow['lport'] == ifstate.get('if-index')) or
                (iface['name'] == flow.get('ifname'))):
            result = 'Table:{},FlowId:{}{}'.format(
                flow['table'], flow['id'],
                utils.show_optionals(flow))
            print(result)
            print("Flow: {}".format(utils.format_json(None, flow_parser.parse_flow(flow.get('flow')))))


def analyze_inventory(args):
    config.get_models(args, {
        "odl_inventory_nodes_config",
        "odl_inventory_nodes_operational"})

    if args.store == "config":
        nodes = config.gmodels.odl_inventory_nodes_config.get_clist_by_key()
        print("Inventory Config:")
    else:
        print("Inventory Operational:")
        nodes = config.gmodels.odl_inventory_nodes_operational.get_clist_by_key()
    node = nodes.get("openflow:" + args.nodeid)
    if node is None:
        print("node: {} was not found".format("openflow:" + args.nodeid))
        return
    tables = node.get(Nodes.NODE_TABLE)
    # groups = node.get(Nodes.NODE_GROUP)
    flow_list = []
    print("Flows: ")
    for table in tables:
        for flow in table.get('flow', []):
            if not args.ifname or args.ifname in utils.nstr(flow.get('flow-name')):
                flow_dict = {'table': table['id'], 'id': flow['id'], 'name': flow.get('flow-name'), 'flow': flow}
                flow_list.append(flow_dict)
    flowlist = sorted(flow_list, key=lambda x: x['table'])
    for flow in flowlist:
        print("Table: {}".format(flow['table']))
        print("FlowId: {}, FlowName: {} ".format(flow['id'], 'FlowName:', flow.get('name')))


def analyze_nodes(args):
    config.get_models(args, {
        "ietf_interfaces_interfaces",
        "itm_state_dpn_endpoints",
        "neutron_neutron",
        "odl_inventory_nodes_operational"})
    nodes = config.gmodels.itm_state_dpn_endpoints.get_clist_by_key()

    noded = {}
    ports_by_name = {}

    # for k, v in nodes.items():
    #     dpn_id = v.get(DpnEndpoints.DPN_ID)
    #     ip = config.gmodels.itm_state_dpn_endpoints.get_ip_address_from_dpn_info(v)
    #     attrs = {"dpn_id": dpn_id, "ip": ip}
    #     noded[dpn_id] = attrs

    nodes = config.gmodels.odl_inventory_nodes_operational.get_clist_by_key()
    for k, v in nodes.items():
        dpn_id = k.split(":")[1]
        ip = v.get("flow-node-inventory:ip-address")
        ovs_version = v.get("flow-node-inventory:software")
        node_connectors = v.get("node-connector")

        ports = {}
        for port in node_connectors:
            port_no = port.get("flow-node-inventory:port-number")
            if port_no == 0xfffffffe:
                port_no = 0
            name = port.get("flow-node-inventory:name")
            port_attrs = {"port_no": port_no,
                          "mac": port.get("flow-node-inventory:hardware-address"),
                          "name": name}
            ports[port_no] = port_attrs
            ports_by_name[name] = port_attrs
        attrs = {"dpn_id": dpn_id, "ip": ip, "ovs_version": ovs_version, "ports": ports}
        noded[dpn_id] = attrs

    # neutron_ports = config.gmodels.neutron_neutron.get_objects_by_key(obj=Neutron.PORTS)
    ifaces = config.gmodels.ietf_interfaces_interfaces.get_clist_by_key()
    for iface_name, iface in ifaces.items():
        for port_name, port in ports_by_name.items():
            if iface_name == port_name:
                ip = iface.get("odl-interface:tunnel-source")
                # ip =

    print("\nnodes\n")
    for k, v in sorted(noded.items()):
        dpn_id = v.get("dpn_id")
        ip = v.get("ip")
        print("dpn-id: {}, ip: {}".format(dpn_id, ip))

    for k, v in sorted(noded.items()):
        dpn_id = k
        ip = v.get("ip")
        ovs_version = v.get("ovs_version")
        print("\ndpn-id: {}, ip: {}, version: {}".format(dpn_id, ip, ovs_version))
        ports = v.get("ports")
        for port_no, port_attrs in sorted(ports.items()):
            print("{:3} {} {:14} {:15}".format(
                port_attrs.get("port_no"), port_attrs.get("mac"), port_attrs.get("name"),
                port_attrs.get("ip")))
