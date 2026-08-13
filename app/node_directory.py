from dataclasses import dataclass


@dataclass(frozen=True)
class DataNode:
    name: str
    host: str
    port: int


DATA_NODES = {
    "customer": DataNode(
        name="customer-node-1",
        host="localhost",
        port=5432,
    ),
}


def get_node_for_data(data_type: str) -> DataNode | None:
    """Return the node responsible for a data type."""
    return DATA_NODES.get(data_type)