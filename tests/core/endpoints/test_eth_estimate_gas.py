CONTRACT_BIN = b'0x6060604052610114806100126000396000f360606040526000357c01000000000000000000000000000000000000000000000000000000009004806316216f391461004f578063a5f3c23b14610072578063dcf537b1146100a75761004d565b005b61005c60048050506100d3565b6040518082815260200191505060405180910390f35b61009160048080359060200190919080359060200190919050506100e6565b6040518082815260200191505060405180910390f35b6100bd60048080359060200190919050506100fd565b6040518082815260200191505060405180910390f35b6000600d905080508090506100e3565b90565b6000818301905080508090506100f7565b92915050565b6000600782029050805080905061010f565b91905056'  # noqa E501


def test_eth_estimate_gas(rpc_client, accounts):
    hex_gas_estimate = rpc_client(
        method="eth_estimateGas",
        params=[{
            "from": accounts[0],
            "data": CONTRACT_BIN,
            "value": 1234,
        }],
    )
    gas_estimate = hex_gas_estimate
    assert gas_estimate > 50000


def test_eth_estimate_gas_hex_value(rpc_client, accounts):
    hex_gas_estimate = rpc_client(
        method="eth_estimateGas",
        params=[{
            "from": accounts[0],
            "data": CONTRACT_BIN,
            "value": hex(1234),
        }],
    )
    gas_estimate = hex_gas_estimate
    assert gas_estimate > 50000
