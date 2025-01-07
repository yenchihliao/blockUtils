// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Script.sol";
import "forge-std/Test.sol";
import "forge-std/console.sol";

import {SwissKnife} from "../src/SwissKnife.sol";

abstract contract StubInbox {
    function unsafeCreateRetryableTicket(
        address to,
        uint256 l2CallValue,
        uint256 maxSubmissionCost,
        address excessFeeRefundAddress,
        address callValueRefundAddress,
        uint256 gasLimit,
        uint256 maxFeePerGas,
        bytes calldata data
    ) virtual external payable returns (uint256);

    function calculateRetryableSubmissionFee(uint256 dataLength, uint256 baseFee)
    virtual public view returns (uint256);

    function estimateRetryableTicket(
        address sender,
        uint256 deposit,
        address to,
        uint256 l2CallValue,
        address excessFeeRefundAddress,
        address callValueRefundAddress,
        bytes calldata data
    ) virtual external;

    event MessageDelivered( uint256 indexed messageIndex, bytes32 indexed beforeInboxAcc, address inbox, uint8 kind, address sender, bytes32 messageDataHash, uint256 baseFeeL1, uint64 timestamp);
    event InboxMessageDelivered(uint256 indexed messageNum, bytes data);
    event RedeemScheduled(bytes32 indexed ticketId, bytes32 indexed retryTxHash, uint64 indexed sequenceNum, uint64 donatedGas, address gasDonor, uint256 maxRefund, uint256 submissionFeeRefund);
}
// Usage: forg script --rpc-url $L1_URL --private-key $KEY "script/SendUnsafeCreateRetryableTicket.s.sol:SendUnsafeCreateRetryableTicket"
contract SendUnsafeCreateRetryableTicket is Test, Script {
    modifier broadcastAll() {
        vm.startBroadcast();
        _;
        vm.stopBroadcast();
    }
    function run() external {
        // StubInbox _inbox__ = StubInbox(0xaAe29B0366299461418F5324a79Afc425BE5ae21); // sepolia
        StubInbox _inbox__ = StubInbox(0x4Dbd4fc535Ac27206064B68FfCf827b0A60BAB3f); // Eth

        // SwissKnife _swissKnife__ = SwissKnife(0x2b223c44C2Ad3f1cFf0022e91c87ad7DbfA05026); // arb sepolia
        SwissKnife _swissKnife__ = SwissKnife(0x78046053E5B02Ca2056D7007cf55747244223E5B); // Eth
        address _receiver = 0x95244948C80B46c9f196d42e80635C254F6d9f14; // xsync vault
        address _receiver2 = 0x51c289a2C7aE30BC39D60F0d210cC17FA15C8950;
        address _receiver3 = 0x51c289a2C7aE30BC39D60F0d210cC17FA15C8950;
        uint256 _bridgeAmount = 1 wei;

        // Get the maxSubmissionCost on L1
        uint256 _maxSubmissionCost = _inbox__.calculateRetryableSubmissionFee(0, 0);
        require(_maxSubmissionCost == block.basefee * 1400); // L1 block.basefee * 1400
        _maxSubmissionCost *= 2;

        // Get the gasLimit on L2
        // Transfer only takes 21000 gas
        uint256 _gasLimit = 100000;

        // Get the maxFeePerGas on L2
        // tx.gasprice
        // $cast rpc -r $URL eth_gasPrice
        uint256 _maxFeePerGas = 1e7;
        _maxFeePerGas *= 2;

        bytes memory _calldata = abi.encodeWithSelector(
            _inbox__.unsafeCreateRetryableTicket.selector,
            _receiver,
            _bridgeAmount,
            _maxSubmissionCost,
            _receiver2,
            _receiver3,
            _gasLimit,
            _maxFeePerGas,
            ""
        );

        uint256 _inputAmount = _bridgeAmount + _maxSubmissionCost + _maxFeePerGas * _gasLimit;
        console.log("Input amount: %d", _inputAmount);
        vm.startBroadcast();
        _swissKnife__.delegateForward{value: _inputAmount}(address(_inbox__), _calldata);
        // address(_inbox__).call{value: _inputAmount}(_calldata);
        vm.stopBroadcast();
    }
}
