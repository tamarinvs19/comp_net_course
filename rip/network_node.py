from __future__ import annotations
from dataclasses import dataclass
import time
from threading import Lock
from typing import Final, Generic, IO, Optional, TypeVar
import sys

from edge import Edge

TNetwork = TypeVar('TNetwork')


class NetworkNode(Generic[TNetwork]):
    def __init__(
        self,
        ip_address: str = '0.0.0.0',
        current_network: TNetwork = None,
        simulation_cycles: int = 0
    ) -> None:
        self.ip_address = ip_address
        self.current_network = current_network
        self.simulation_cycles = simulation_cycles
        self.edges: set[Edge[NetworkNode]] = set()
        self.table: RoutingTable

        self.thread_lock = Lock()

    def __hash__(self) -> int:
        return hash(self.ip_address)

    def __repr__(self) -> str:
        return '<NetworkNode(ip_address={0})'.format(self.ip_address)

    def __str__(self) -> str:
        return self.ip_address

    def init_table(self) -> None:
        self.table = RoutingTable(self, self.current_network)

    def receive(self, node: NetworkNode, received_table: RoutingTable) -> None:
        with self.thread_lock:
            for state in received_table.states:
                if state.next_node.ip_address == '0.0.0.0':
                    continue

                current_states = self.table.states
                for i, current_state in enumerate(current_states):
                    if current_state.destination_node == state.destination_node:
                        target_metric = state.metric + 1
                        if target_metric < current_state.metric:
                            current_state.metric = target_metric
                            current_state.next_node = node
                            self.table.states[i] = current_state

    def broadcast(self) -> None:
        for edge in self.edges:
            node = edge.right if edge.left == self else edge.left
            if node is not None:
                node.receive(self, self.table)

    def simulate(self, file_name: str = '') -> None:
        for i in range(self.simulation_cycles):
            output = self.table.make_output_table(i+1)
            if file_name == '':
                print(output)
            else:
                with open(file_name, 'at', encoding='utf-8') as fout:
                    print(output, file=fout)
            self.broadcast()
            time.sleep(1)


@dataclass
class RoutingState:
    next_node: NetworkNode
    destination_node: NetworkNode
    metric: int

    def __hash__(self) -> int:
        return hash((self.next_node, self.destination_node, self.metric))


class RoutingTable(Generic[TNetwork]):
    MAX_HOPS: Final = 15

    def __init__(self, node: NetworkNode, network: TNetwork) -> None:
        self.current_network = network
        self.parent_node = node
        self.states: list[RoutingState] = []
        self.init_state()

    def init_state(self) -> None:
        for node in self.current_network.network_nodes:
            next_node: NetworkNode = NetworkNode()
            target_metric = self.MAX_HOPS + 1

            for edge in self.parent_node.edges:
                if edge.left == node:
                    if edge.left.ip_address == '0.0.0.0':
                        continue
                    next_node = edge.left
                    target_metric = 1
                    break
                if edge.right == node:
                    if edge.right.ip_address == '0.0.0.0':
                        continue
                    next_node = edge.right
                    target_metric = 1
                    break
            self.states.append(
                RoutingState(
                    next_node,
                    node,
                    target_metric,
                )
            )
    def make_output_table(self, step: int = -1) -> str:
        output_text: list[str] = []
        if step != -1:
            output_text.append(
                'Simulation step {0} of router {1}'.format(
                    step,
                    self.parent_node.ip_address,
                )
            )
        output_text.append(
            '[Sourse IP]\t[Destination IP]\t[Next Hop]\t[Metric]',
        )
        for state in self.states:
            if self.parent_node == state.destination_node or state.next_node.ip_address == '0.0.0.0':
                continue
            output_text.append(
                '{0}\t{1}\t\t{2}\t{3}'.format(
                    self.parent_node.ip_address,
                    state.destination_node.ip_address,
                    state.next_node.ip_address,
                    'inf' if state.metric > self.MAX_HOPS + 1 else state.metric
                ),
            )
        return '\n'.join(output_text) + '\n'

