
def test_eth_blockNumber(rpc_client):
    result = rpc_client('eth_blockNumber')
    assert result == 0
