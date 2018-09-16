from eth_utils import (
    big_endian_to_int,
    encode_hex,
    decode_hex,
    keccak,
)


CONTRACT_BIN = '0x6060604052610114806100126000396000f360606040526000357c01000000000000000000000000000000000000000000000000000000009004806316216f391461004f578063a5f3c23b14610072578063dcf537b1146100a75761004d565b005b61005c60048050506100d3565b6040518082815260200191505060405180910390f35b61009160048080359060200190919080359060200190919050506100e6565b6040518082815260200191505060405180910390f35b6100bd60048080359060200190919050506100fd565b6040518082815260200191505060405180910390f35b6000600d905080508090506100e3565b90565b6000818301905080508090506100f7565b92915050565b6000600782029050805080905061010f565b91905056'


CONTRACT_BIN_RUNTIME = '0x60606040526000357c01000000000000000000000000000000000000000000000000000000009004806316216f391461004f578063a5f3c23b14610072578063dcf537b1146100a75761004d565b005b61005c60048050506100d3565b6040518082815260200191505060405180910390f35b61009160048080359060200190919080359060200190919050506100e6565b6040518082815260200191505060405180910390f35b6100bd60048080359060200190919050506100fd565b6040518082815260200191505060405180910390f35b6000600d905080508090506100e3565b90565b6000818301905080508090506100f7565b92915050565b6000600782029050805080905061010f565b91905056'

CONTRACT_SOURCE = """ 
contract Math {
    uint public counter;

    event Increased(uint value);

    function increment() public returns (uint) {
        return increment(1);
    }

    function increment(uint amt) public returns (uint result) {
        counter += amt;
        result = counter;
        Increased(result);
        return result;
    }

    function add(int a, int b) public returns (int result) {
        result = a + b;
        return result;
    }

    function multiply7(int a) public returns (int result) {
        result = a * 7;
        return result;
    }

    function return13() public returns (int result) {
        result = 13;
        return result;
    }
}
"""


def test_eth_call(rpc_client, accounts):
    txn_hash = rpc_client(
        method="eth_sendTransaction",
        params=[{
            "from": accounts[0],
            "data": CONTRACT_BIN,
            "value": 1234,
            "gas": 3144659,
        }],
    )
    txn_receipt = rpc_client(
        method="eth_getTransactionReceipt",
        params=[txn_hash],
    )
    contract_address = txn_receipt['contractAddress']

    assert contract_address

    function_sig = encode_hex(keccak(text="return13()")[:4])

    should_be_13 = rpc_client(
        method="eth_call",
        params=[{
            "from": accounts[0],
            "to": contract_address,
            "data": function_sig,
            "gas": 3144659,
        }],
    )

    result = big_endian_to_int(decode_hex(should_be_13[2:]))
    assert result == 13
