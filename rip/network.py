import json
from threading import Thread
from typing import Optional

from network_node import NetworkNode
from edge import Edge


class Network:
    def __init__(self) -> None:
        self.network_nodes: set[NetworkNode] = set()

    def json_load(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as fin:
            data = json.load(fin)
            simulation_cycles = data['simulation_cycles']
            networks = data['networks']
            ips: dict[str, NetworkNode] = {}
            for network_ip, neighbors in networks.items():
                if network_ip not in ips:
                    node = NetworkNode(network_ip, self, simulation_cycles)
                    ips[network_ip] = node
                else:
                    node = ips[network_ip]

                for neighbor_ip in neighbors:
                    if neighbor_ip not in ips:
                        neigbor = NetworkNode(
                            neighbor_ip,
                            self,
                            simulation_cycles,
                        )
                        ips[neighbor_ip] = neigbor
                    else:
                        neigbor = ips[neighbor_ip]
                    edge = Edge(node, neigbor)
                    node.edges.add(edge)
                    neigbor.edges.add(edge)
        self.network_nodes = set(ips.values())

    def find_node(self, ip: str) -> Optional[NetworkNode]:
        for node in self.network_nodes:
            if node.ip_address == ip:
                return node
        return None

    def add_link(self, ip1: str, ip2: str) -> None:
        selected1 = self.find_node(ip1)
        selected2 = self.find_node(ip2)

        if selected1 is None or selected2 is None:
            print('One or both routers are not found!')
            return

        edge = Edge(selected1, selected2)
        selected1.edges.add(edge)
        selected2.edges.add(edge)
        print('Link added!')


    def remove_link(self, ip1: str, ip2: str) -> None:
        selected1 = self.find_node(ip1)
        selected2 = self.find_node(ip2)

        if selected1 is None or selected2 is None:
            print('One or both routers are not found!')
            return
        
        selected_edge: Optional[Edge] = None
        for edge in selected1.edges:
            if edge.left == selected1 or edge.right == selected2:
                selected_edge = edge

        if selected_edge is None:
            print('Link not found!')
            return

        selected1.edges.remove(selected_edge)
        selected2.edges.remove(selected_edge)
        print('Link removed!')

    def add_router(self, ip: str) -> None:
        selected = self.find_node(ip)
        if selected is None:
            print('Router not found!')
            return

        self.network_nodes.add(NetworkNode(ip, self))
        print('Router {0} added'.format(ip))

    def remove_router(self, ip: str) -> None:
        selected = self.find_node(ip)
        if selected is None:
            print('Router not found!')
            return

        self.network_nodes.remove(selected)
        for node in self.network_nodes:
            edges = node.edges
            for edge in edges:
                if edge.left == selected or edge.right == selected:
                    node.edges.remove(edge)
        print('Router {0} removed'.format(ip))

    def simulate(self, simulation_cycles: Optional[int] = None, file_name: str = '') -> None:
        if file_name != '':
            with open(file_name, 'w', encoding='utf-8'):
                pass

        threads: set[Thread] = set()
        for node in self.network_nodes:
            node.init_table()

        for node in self.network_nodes:
            if simulation_cycles is not None:
                node.simulation_cycles = simulation_cycles

            thread = Thread(
                target=node.simulate,
                kwargs={'file_name': file_name},
            )
            threads.add(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for node in self.network_nodes:
            output = [
                'Final state of router {0} table:'.format(
                    node.ip_address
                ),
                node.table.make_output_table(),
            ]
            if file_name == '':
                print('\n'.join(output))
            else:
                with open(file_name, 'at', encoding='utf-8') as fout:
                    print('\n'.join(output), file=fout)

