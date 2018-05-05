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

from odltools.mdsal.models.model import Model

MODULE = "network-topology"


def network_topology(store, args, mid="ovsdb:1"):
    return NetworkTopology(MODULE, store, args, mid)


class NetworkTopology(Model):
    # TODO: class currently assumes the ovsdb:1 has been used so need to fix that to take a topology-id
    CONTAINER = "network-topology"
    TOPOLOGY = "topology"
    NODE = "node"
    OVSDB1 = "ovsdb:1"

    def get_clist(self):
        return self.data[self.TOPOLOGY]

    def get_topology_by_tid(self, tid="ovsdb:1"):
        topologies = self.get_clist()
        for topology in topologies:
            if topology['topology-id'] == tid:
                return topology
        return {}

    def get_nodes_by_tid(self, tid="ovsdb:1"):
        topology = self.get_topology_by_tid(tid)
        return topology.get(self.NODE, [])

    def get_nodes_by_tid_and_key(self, tid="ovsdb:1", key='node-id'):
        d = {}
        nodes = self.get_nodes_by_tid(tid)
        for node in nodes:
            d[node[key]] = node
        return d
