from math import e
from eth_utils import keccak, to_bytes, to_hex
from web3 import Web3
from rlp import encode as rlp_encode
from hexbytes import HexBytes

def calculate_submit_retryable_id(
    l2_chain_id: int,
    from_address: str,
    message_number: int,
    l1_base_fee: int,
    dest_address: str,
    l2_call_value: int,
    l1_value: int,
    max_submission_fee: int,
    excess_fee_refund_address: str,
    call_value_refund_address: str,
    gas_limit: int,
    max_fee_per_gas: int,
    data: str
) -> str:
    def format_number(value: int) -> bytes:
        print(f'formatting: {value}')
        ret = bytes.fromhex(HexBytes(value).hex())
        print(f'formatted: {ret.hex()}')
        return ret

    # Convert inputs to byte format and pad where necessary
    fields = [
        format_number(l2_chain_id),
        format_number(message_number).rjust(32, b'\x00'),
        Web3.to_bytes(hexstr=from_address),
        format_number(l1_base_fee),
        format_number(l1_value),
        format_number(max_fee_per_gas),
        format_number(gas_limit),
        Web3.to_bytes(hexstr=dest_address),
        format_number(l2_call_value),
        Web3.to_bytes(hexstr=call_value_refund_address),
        format_number(max_submission_fee),
        Web3.to_bytes(hexstr=excess_fee_refund_address),
        Web3.to_bytes(hexstr=data)
    ]
    # Print each field in HexBytes format
    for i, field in enumerate(fields):
        print(f"Field {i}: {HexBytes(field).hex()}")

    # RLP encode the fields with Arbitrum transaction type 0x69
    rlp_encoded = to_hex(b'\x69' + rlp_encode(fields))

    # Calculate and return keccak256 hash
    return Web3.to_hex(keccak(hexstr=rlp_encoded))

# _deliverMessage(
#     L1MessageType_submitRetryableTx,
#     msg.sender,
#     abi.encodePacked(
#         uint256(uint160(to)), [0]
#         l2CallValue, [1]
#         msg.value, [2]
#         maxSubmissionCost, [3]
#         uint256(uint160(excessFeeRefundAddress)), [4]
#         uint256(uint160(callValueRefundAddress)), [5]
#         gasLimit, [6]
#         maxFeePerGas, [7]
#         data.length,  [8]
#         data  [9]
#     )
# );
if __name__ == '__main__':
    l2_chain_id = 42161
    from_address = '0x78046053E5B02Ca2056D7007cf55747244223E5B'
    # inbox_message_delivered index 1
    message_number = 1737018
    # cast base-fee -r 1 block_height
    l1_base_fee = 8317249987
    # inbox_message_delivered[0]
    dest_address = '0x51c289a2C7aE30BC39D60F0d210cC17FA15C8950'
    # inbox_message_delivered[1]
    l2_call_value = 1
    # inbox_message_delivered[2]
    l1_value = 27569394031201
    # inbox_message_delivered[3]
    max_submission_fee = 27149394031200
    # inbox_message_delivered[4]
    excess_fee_refund_address =  '0x856C363E043AC34B19D584D3930BFA615947994E'
    # inbox_message_delivered[5]
    call_value_refund_address = '0x9C9F55EBC51D0D606227790D14AFCB706178DE98'
    # inbox_message_delivered[6]
    gas_limit = 21000
    # inbox_message_delivered[7]
    max_fee_per_gas = 20000000
    # inbox_message_delivered[9]
    data = ''
    predict = calculate_submit_retryable_id(
            l2_chain_id,
            from_address,
            message_number,
            l1_base_fee,
            dest_address,
            l2_call_value,
            l1_value,
            max_submission_fee,
            excess_fee_refund_address,
            call_value_refund_address,
            gas_limit,
            max_fee_per_gas,
            data
        )
    target = "0x62f686d756529746e4fc6c776e712b03f346c17c71af712944dd02b56a7d5e7a"
    print (predict, target)