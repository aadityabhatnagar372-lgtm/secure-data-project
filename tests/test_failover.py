from unittest.mock import patch
from urllib.error import URLError

import pytest

from app.routes import request_customer_email_from_node
from app.node_directory import DataNode


def test_failover_uses_replica_when_primary_is_unavailable():
    primary = DataNode(
        name="customer-node-1",
        host="primary",
        port=8001,
        role="primary",
    )

    replica = DataNode(
        name="customer-node-2",
        host="replica",
        port=8002,
        role="replica",
    )

    calls = []

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b'{"customer_id": 1, "email": "alice@example.com"}'

    def fake_urlopen(request, timeout):
        calls.append(request.full_url)

        if "primary:8001" in request.full_url:
            raise URLError("primary unavailable")

        return FakeResponse()

    with patch(
        "app.routes.get_primary_node",
        return_value=primary,
    ), patch(
        "app.routes.get_replica_nodes",
        return_value=[replica],
    ), patch(
        "app.routes.urlopen",
        side_effect=fake_urlopen,
    ):
        result = request_customer_email_from_node(1)

    assert result == {
        "customer_id": 1,
        "email": "alice@example.com",
    }

    assert calls == [
        "http://primary:8001/customer/1/email",
        "http://replica:8002/customer/1/email",
    ]


def test_failover_raises_503_when_all_nodes_are_unavailable():
    primary = DataNode(
        name="customer-node-1",
        host="primary",
        port=8001,
        role="primary",
    )

    replica = DataNode(
        name="customer-node-2",
        host="replica",
        port=8002,
        role="replica",
    )

    def fake_urlopen(request, timeout):
        raise URLError("node unavailable")

    with patch(
        "app.routes.get_primary_node",
        return_value=primary,
    ), patch(
        "app.routes.get_replica_nodes",
        return_value=[replica],
    ), patch(
        "app.routes.urlopen",
        side_effect=fake_urlopen,
    ):
        with pytest.raises(
            Exception,
            match="All customer data nodes are unavailable",
        ):
            request_customer_email_from_node(1)