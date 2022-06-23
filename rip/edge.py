from __future__ import annotations
from typing import Generic, Optional, TypeVar

TNetworkNode = TypeVar('TNetworkNode')


class Edge(Generic[TNetworkNode]):
    def __init__(
        self,
        left: Optional[TNetworkNode],
        right: Optional[TNetworkNode],
    ):
        self.right = right
        self.left = left

    def __hash__(self) -> int:
        return hash(self.left) + hash(self.right)

    def __eq__(self, other) -> bool:
        straight = self.left == other.left and self.right == other.right
        reverced = self.left == other.right and self.right == other.left
        return straight or reverced

    def __repr__(self):
        return '<Edge(left={0}, right={1})>'.format(
            self.left,
            self.right,
        )

