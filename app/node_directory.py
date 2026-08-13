from dataclasses import dataclass


@dataclass(frozen=True)
class DataNode:
    name: str
    host: str
    port: int
    role: str


DATA_NODES = {
    "customer-primary": DataNode(
        name="customer-node-1",
        host="localhost",
        port=8001,
        role="primary",
    ),
    "customer-replica-1": DataNode(
        name="customer-node-2",
        host="localhost",
        port=8002,
        role="replica",
    ),
    "customer-replica-2": DataNode(
        name="customer-node-3",
        host="localhost",
        port=8003,
        role="replica",
    ),
}


def get_primary_node(data_type: str) -> DataNode | None:
    """Return the primary node for a data type."""
    if data_type == "customer":
        return DATA_NODES["customer-primary"]

    return None


def get_replica_nodes(data_type: str) -> list[DataNode]:
    """Return replica nodes for a data type."""
    if data_type == "customer":
        return [
            DATA_NODES["customer-replica-1"],
            DATA_NODES["customer-replica-2"],
        ]

    return []


def get_node_for_data(data_type: str) -> DataNode | None:
    """Backward-compatible primary-node lookup."""
    return get_primary_node(data_type)