import contextlib
import itertools
import json
import os

from eth_utils import (
    to_text,
)
import pytest

from eth_tester_rpc.utils.compat_threading import (
    make_server,
    spawn,
)
from eth_tester_rpc.utils.conversion import (
    force_obj_to_text,
)
from tests.utils import (
    close_http_socket,
    get_open_port,
    wait_for_http_connection,
)

request_counter = itertools.count()


@pytest.fixture()
def open_port():
    return get_open_port()


@pytest.yield_fixture()
def rpc_server(open_port):
    from eth_tester_rpc.server import get_application

    application = get_application()

    server = make_server(
        '127.0.0.1',
        open_port,
        application,
    )
    thread = spawn(server.serve_forever)
    wait_for_http_connection(open_port)

    yield server
    close_http_socket(open_port)
    try:
        server.stop()
    except AttributeError:
        server.shutdown()

    thread.join()


@pytest.fixture()
def rpc_client(rpc_server):
    try:
        host, port = rpc_server.address
    except AttributeError:
        host, port = rpc_server.server_address

    endpoint = "http://{host}:{port}".format(host=host, port=port)

    def make_request(method, params=None):
        global request_counter
        payload = {
            "id": next(request_counter),
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
        }
        payload_data = json.dumps(force_obj_to_text(payload, True))

        if 'TESTRPC_ASYNC_GEVENT' in os.environ:
            from geventhttpclient import HTTPClient
            client = HTTPClient(
                host=host,
                port=port,
                connection_timeout=10,
                network_timeout=10,
                headers={
                    'Content-Type': 'application/json',
                },
            )
            with contextlib.closing(client):
                response = client.post('/', body=payload_data)
                response_body = response.read()

            result = json.loads(to_text(response_body))
        else:
            import requests
            response = requests.post(
                endpoint,
                data=payload_data,
                headers={
                    'Content-Type': 'application/json',
                },
            )

            result = response.json()

        if 'error' in result:
            raise AssertionError(result['error'])

        return result['result']

    make_request.server = rpc_server

    return make_request
